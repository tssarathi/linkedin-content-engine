# Autonomous Agent Rebuild — Design Document
**Date:** 2026-02-23
**Status:** Approved
**Branch:** to be created

---

## 1. Problem Statement

The current system follows a hardcoded deterministic flow: every agent always runs, order is fixed in `orchestrator.py`, and two separate frameworks (LangGraph for research, Google ADK for content) are glued together. This is a pipeline, not an agent.

The goal is to rebuild the orchestration layer as a true autonomous ReAct agent that:
- Decides which agents to call and in what order
- Skips agents that aren't needed for a given input
- Runs independent agents in parallel via parallel tool calling
- Enforces quality gates through an internal content subgraph loop
- Lives entirely within one framework: LangGraph

---

## 2. What Changes vs What Stays

### Stays (untouched)
- All 9 agent logic files (`research_agent/agents/`, `content_agent/agents/`)
- All Pydantic schemas (`research_agent/schemas/`, `content_agent/schemas/`)
- All prompt files (`research_agent/prompts/`, `content_agent/prompts/`)
- All MCP tool integrations (GitHub, Exa, Tavily)
- `shared/config.py`, `shared/logger.py`, `shared/prompt_parser.py`
- `main.py`

### Deleted
- `pipeline/orchestrator.py` — replaced by `agent/master.py`
- `content_agent/pipeline.py` — replaced by `agent/subgraphs/content.py`
- `research_agent/graph.py` — replaced by `@tool` wrappers

### Added
- `agent/master.py` — ReAct master agent
- `agent/state.py` — unified AgentState TypedDict
- `agent/tools/research_tools.py` — `@tool` wrappers for 6 research agents
- `agent/tools/content_tools.py` — `@tool` wrapper for content pipeline
- `agent/subgraphs/content.py` — LangGraph content subgraph (replaces ADK SequentialAgent + LoopAgent)
- `pipeline/__init__.py` — updated to call master agent

---

## 3. Architecture

```
main.py
  └── run_pipeline(user_input)
        ├── parse_prompt(user_input) → (request, repo_url)   [preprocessing, no LLM]
        └── master_agent.ainvoke(request, repo_url)
              │
              │  ReAct Master (Groq llama-3.3-70b)
              │  Thought → Action → Observation loop
              │
              ├── github_analyser_tool(repo_url)         → ProjectAnalysis
              ├── supervisor_tool(request, analysis)     → SupervisorOutput
              ├── [news_researcher_tool  ◄─── PARALLEL
              ├──  trend_analyser_tool]  ◄─── PARALLEL   → NewsFindings, TrendData
              ├── fact_checker_tool(claims)              → FactCheckResults
              ├── synthesizer_tool(all_findings)         → ResearchBrief
              └── run_content_pipeline_tool(brief)       → LinkedInPost
                        │
                        └── content subgraph (internal)
                              strategist → copywriter → editor
                                                ↑          │
                                                └──revise───┘ (max 2x)
                                                           │
                                                        approve
                                                           │
                                                       optimizer
```

---

## 4. Unified State

```python
# agent/state.py
class AgentState(TypedDict):
    # Input
    user_input: str
    request: str
    repo_url: Optional[str]

    # Research outputs
    project_analysis: Optional[ProjectAnalysis]
    supervisor_output: Optional[SupervisorOutput]
    news_findings: Optional[NewsFindings]
    trend_data: Optional[TrendData]
    fact_check_results: Optional[FactCheckResults]
    research_brief: Optional[ResearchBrief]

    # Content outputs
    strategy_document: Optional[StrategyDocument]
    post_draft: Optional[str]
    editor_review: Optional[EditorReview]
    revision_count: int
    linkedin_post: Optional[LinkedInPost]

    # ReAct internals
    messages: Annotated[list, add_messages]
```

---

## 5. Tool Wrappers

Each existing agent is wrapped in a `@tool` decorated async function. The docstring is the agent's signal to the master — written precisely to guide tool selection and parallel batching.

```python
# agent/tools/research_tools.py

@tool
async def github_analyser_tool(repo_url: str) -> dict:
    """Analyzes a GitHub repository. Returns tech stack, key features, recent
    activity, and project summary. Call this FIRST if a GitHub URL is provided."""

@tool
async def supervisor_tool(request: str, project_analysis: Optional[dict]) -> dict:
    """Determines post type, extracts buzzwords for keyword search, and creates
    project context for semantic search. Call after github_analyser_tool (or
    directly if no GitHub URL)."""

@tool
async def news_researcher_tool(buzzwords: list[str]) -> dict:
    """Searches for recent news articles using keyword (BM25) search.
    Independent of trend analysis — can run simultaneously with trend_analyser_tool."""

@tool
async def trend_analyser_tool(project_context: str) -> dict:
    """Discovers trending topics using semantic (neural) search via Exa.
    Independent of news research — can run simultaneously with news_researcher_tool."""

@tool
async def fact_checker_tool(claims: list[str]) -> dict:
    """Verifies specific claims from news and trend findings. Call after both
    news_researcher_tool and trend_analyser_tool have completed."""

@tool
async def synthesizer_tool(
    request: str,
    project_analysis: Optional[dict],
    supervisor_output: dict,
    news_findings: dict,
    trend_data: dict,
    fact_check_results: dict,
) -> dict:
    """Combines all research findings into a structured ResearchBrief.
    Call only after all research tools have completed."""

@tool
async def run_content_pipeline_tool(research_brief: dict) -> dict:
    """Runs the full content pipeline: strategy → copywriting → editorial review
    loop (max 2 iterations) → final optimization. Returns a publish-ready
    LinkedIn post. Call this last, after synthesizer_tool."""
```

---

## 6. Content Subgraph (ADK → LangGraph)

The ADK `SequentialAgent` + `LoopAgent` pattern is replaced with explicit LangGraph nodes and a conditional edge.

```python
# agent/subgraphs/content.py

def should_revise(state: AgentState) -> str:
    review = state["editor_review"]
    iteration = state.get("revision_count", 0)
    if review.approved or iteration >= 2:
        return "optimizer"
    return "copywriter"

content_graph = StateGraph(AgentState)
content_graph.add_node("strategist", run_strategist_node)
content_graph.add_node("copywriter", run_copywriter_node)
content_graph.add_node("editor", run_editor_node)
content_graph.add_node("optimizer", run_optimizer_node)

content_graph.set_entry_point("strategist")
content_graph.add_edge("strategist", "copywriter")
content_graph.add_edge("copywriter", "editor")
content_graph.add_conditional_edges("editor", should_revise, {
    "optimizer": "optimizer",
    "copywriter": "copywriter",
})
content_graph.add_edge("optimizer", END)
```

Each node function wraps the existing agent:
```python
async def run_strategist_node(state: AgentState) -> dict:
    result = await strategist_agent_logic(state["research_brief"])
    return {"strategy_document": result}
```

---

## 7. ReAct Master Agent

```python
# agent/master.py

from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq

SYSTEM_PROMPT = """
You are a LinkedIn content strategist. Produce a publish-ready LinkedIn post
from the user's request using the tools available to you.

Follow this sequence:
1. If repo_url is present in context, call github_analyser_tool first
2. Call supervisor_tool with the request (and project_analysis if available)
3. Call news_researcher_tool AND trend_analyser_tool together (they are independent)
4. Call fact_checker_tool with key claims from news and trends
5. Call synthesizer_tool with all gathered findings
6. Call run_content_pipeline_tool with the research brief

Return only the publish_ready_post string from the final result. Nothing else.
"""

tools = [
    github_analyser_tool,
    supervisor_tool,
    news_researcher_tool,
    trend_analyser_tool,
    fact_checker_tool,
    synthesizer_tool,
    run_content_pipeline_tool,
]

master_agent = create_react_agent(
    model=ChatGroq(model="llama-3.3-70b-versatile", temperature=0),
    tools=tools,
    state_modifier=SYSTEM_PROMPT,
    recursion_limit=25,
)
```

---

## 8. Entry Point Update

```python
# pipeline/__init__.py

async def run_pipeline(user_input: str) -> str:
    request, repo_url = parse_prompt(user_input)

    initial_state = {
        "messages": [HumanMessage(content=request)],
        "repo_url": repo_url,
        "request": request,
    }

    result = await master_agent.ainvoke(initial_state)

    # Extract final post from last AI message
    return result["messages"][-1].content
```

---

## 9. Parallel Tool Calling

`news_researcher_tool` and `trend_analyser_tool` run in parallel via the LLM outputting both tool calls in a single response turn. LangGraph's `ToolNode` detects multiple tool calls and executes them concurrently with `asyncio.gather`.

The tool docstrings explicitly signal independence with the phrase "can run simultaneously with [other_tool]" to guide the LLM toward batching these calls.

---

## 10. Error Handling

Each `@tool` wrapper catches exceptions and returns a structured error dict:

```python
@tool
async def news_researcher_tool(buzzwords: list[str]) -> dict:
    try:
        ...
    except Exception as e:
        return {"error": str(e), "status": "failed", "news_items": []}
```

The master agent observes the error in its next turn and can reason about it (retry, skip, or proceed with partial data). The `recursion_limit=25` prevents runaway loops.

---

## 11. New File Structure

```
linkedin-content-engine/
├── main.py                              # unchanged
├── shared/                              # unchanged
├── research_agent/
│   ├── agents/                          # unchanged — all 6 agent files
│   ├── schemas/                         # unchanged
│   └── prompts/                         # unchanged
│   # graph.py DELETED
├── content_agent/
│   ├── agents/                          # unchanged — all 4 agent files
│   ├── schemas/                         # unchanged
│   └── prompts/                         # unchanged
│   # pipeline.py DELETED
├── agent/                               # NEW
│   ├── master.py                        # ReAct master
│   ├── state.py                         # Unified AgentState
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── research_tools.py            # @tool wrappers for research agents
│   │   └── content_tools.py             # @tool wrapper for content pipeline
│   └── subgraphs/
│       ├── __init__.py
│       └── content.py                   # LangGraph content subgraph
└── pipeline/
    └── __init__.py                      # updated — calls master_agent
```

---

## 12. Key Concepts Demonstrated

| Concept | Where |
|---|---|
| ReAct (Reason + Act) loop | `agent/master.py` |
| Parallel tool calling | news + trend tools called simultaneously |
| Agent-as-tool pattern | `agent/tools/research_tools.py` |
| Conditional graph edges | `agent/subgraphs/content.py` |
| Structured outputs (Pydantic) | All schemas, unchanged |
| Quality gates | Editor node + `should_revise` conditional |
| MCP tool integration | Research agents, unchanged |
| Unified state management | `agent/state.py` |
