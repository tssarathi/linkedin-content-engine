# LinkedIn Content Engine

An AI-powered multi-agent system that transforms a user prompt into a publish-ready LinkedIn post. It combines a **research pipeline** (LangGraph) with a **content generation pipeline** (Google ADK) to produce well-researched, engaging posts — with optional GitHub repository analysis.

## How It Works

```
User Prompt (+ optional GitHub URL)
          │
          ▼
┌─────────────────────────────────────────┐
│         RESEARCH PIPELINE (LangGraph)   │
│                                         │
│  ┌──────────────┐   ┌──────────────┐    │
│  │   GitHub     │──▶│  Supervisor  │    │
│  │   Analyser   │   │              │    │
│  └──────────────┘   └──────┬───────┘    │
│                       ┌────┴────┐       │
│                       ▼         ▼       │
│              ┌──────────┐ ┌──────────┐  │
│              │  News    │ │  Trend   │  │
│              │Researcher│ │ Analyser │  │
│              └────┬─────┘ └────┬─────┘  │
│                   └─────┬──────┘        │
│                         ▼               │
│                  ┌────────────┐         │
│                  │Fact Checker│         │
│                  └─────┬──────┘         │
│                        ▼                │
│                 ┌─────────────┐         │
│                 │ Synthesizer │         │
│                 └─────────────┘         │
└──────────────────────┬──────────────────┘
                       │ Research Brief
                       ▼
┌─────────────────────────────────────────┐
│       CONTENT PIPELINE (Google ADK)     │
│                                         │
│  ┌────────────┐                         │
│  │ Strategist │                         │
│  └─────┬──────┘                         │
│        ▼                                │
│  ┌─────────────────────────┐            │
│  │  Writing Team (loop ×2) │            │
│  │  ┌────────────┐         │            │
│  │  │ Copywriter │◀──┐     │            │
│  │  └─────┬──────┘   │     │            │
│  │        ▼          │     │            │
│  │  ┌──────────┐     │     │            │
│  │  │  Editor  │─────┘     │            │
│  │  └──────────┘  revise   │            │
│  └─────────┬───────────────┘            │
│            ▼                            │
│     ┌────────────┐                      │
│     │ Optimizer  │                      │
│     └────────────┘                      │
└──────────────────────┬──────────────────┘
                       │
                       ▼
              Publish-Ready LinkedIn Post
```

## Research Service

| Agent | Role | Tools |
|-------|------|-------|
| **GitHub Analyser** | Extracts tech stack, features, and summary from a GitHub repo | GitHub MCP (`get_file_contents`, `list_commits`) |
| **Supervisor** | Determines post type, extracts buzzwords for keyword search and project context for semantic search | GPT-4o-mini |
| **News Researcher** | Finds recent news articles related to the topic (last 90 days) | Google Serper |
| **Trend Analyser** | Discovers trending topics and discussions via semantic search | Exa MCP (`web_search_exa`) |
| **Fact Checker** | Verifies claims from the research service against independent sources | Tavily MCP (`tavily_search`) |
| **Synthesizer** | Combines all findings into a structured research brief | GPT-4o-mini |

## Content Service

| Agent | Role |
|-------|------|
| **Strategist** | Analyzes the research brief and produces a strategy document (post type, hook style, CTA, tone) |
| **Copywriter** | Writes the initial draft based on the strategy (under 1,500 chars, mobile-first formatting) |
| **Editor** | Scores the draft on hook strength, authenticity, and value density (1–10 rubric) — approves or requests revision |
| **Optimizer** | Produces the final post with 3 hook variants, hashtags, and a copy-paste ready output |

## Project Structure

```
linkedin-content-engine/
├── pyproject.toml                 # Project metadata & dependencies (v2.0.0)
├── requirements.txt               # Flat dependency list
│
└── app/
    ├── config/
    │   └── config.py              # Centralised environment variable loader
    │
    ├── utilities/
    │   ├── logger.py              # Dual-output logging (DEBUG → file, INFO → console)
    │   └── prompt_parser.py       # Extracts GitHub URLs from user input
    │
    └── core/
        ├── linkedin_content_engine.py # CLI entry point & pipeline orchestration
        ├── research_service/
        │   ├── graph.py           # LangGraph StateGraph definition
        │   ├── state.py           # ResearchState TypedDict
        │   ├── agents/            # Agent implementations
        │   ├── schemas/           # Pydantic output schemas
        │   └── prompts/           # System prompts
        │
        └── content_service/
            ├── agent.py           # Root agent (SequentialAgent)
            ├── agents/            # Agent implementations
            ├── schemas/           # Pydantic output schemas
            └── prompts/           # Agent instructions
```

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js (for MCP servers via `npx`)
- API keys (see below)

### Installation

```bash
git clone https://github.com/sarathisarathi/linkedin-content-engine.git
cd linkedin-content-engine

python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# .venv\Scripts\activate    # Windows

pip install -e .
```

### Environment Variables

Copy `.env.example` to `.env` and fill in the required keys:

```env
# LLM API Keys
OPENAI_API_KEY=              # Used by the research service (GPT-4o-mini)
GOOGLE_API_KEY=              # Used by the content service (Gemini 2.5 Flash Lite)

# Research Service Tool Keys
RS_GA_GITHUB_API_KEY=        # GitHub Personal Access Token
RS_NR_SERPER_API_KEY=        # Google Serper API key
RS_TA_EXA_API_KEY=           # Exa API key
RS_FC_TAVILY_API_KEY=        # Tavily API key

# Observability (optional — auto-read by Langfuse SDK)
LANGFUSE_SECRET_KEY=
LANGFUSE_PUBLIC_KEY=
LANGFUSE_BASE_URL=https://cloud.langfuse.com
```

### Usage

```bash
# With a topic prompt
python -m app.core.linkedin_content_engine "Write a post about the rise of AI agents in developer tooling"

# With a GitHub repo
python -m app.core.linkedin_content_engine "Showcase this project https://github.com/owner/repo"

# Interactive mode
python -m app.core.linkedin_content_engine
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Research orchestration | [LangGraph](https://github.com/langchain-ai/langgraph) |
| Content generation | [Google ADK](https://google.github.io/adk-docs/) |
| Research LLM | [OpenAI GPT-4o-mini](https://platform.openai.com/) |
| Content LLM | [Google Gemini 2.5 Flash Lite](https://ai.google.dev/) |
| Data validation | [Pydantic](https://docs.pydantic.dev/) |
| External search | Google Serper, Exa, Tavily |
| Tool integration | [MCP](https://modelcontextprotocol.io/) (GitHub, Tavily, Exa servers via `npx`) |
| Observability | [Langfuse](https://langfuse.com/) + [OpenInference](https://github.com/Arize-ai/openinference) |

## License

This project is provided as-is for educational and personal use.
