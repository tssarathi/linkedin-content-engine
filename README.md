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

## Research Agents

| Agent | Role | Tools |
|-------|------|-------|
| **GitHub Analyser** | Extracts tech stack, features, and summary from a GitHub repo | GitHub MCP |
| **Supervisor** | Determines post type, extracts buzzwords, creates project context | Groq LLM |
| **News Researcher** | Finds recent news articles related to the topic (last 90 days) | Google Serper |
| **Trend Analyser** | Discovers trending topics and discussions via semantic search | Exa MCP |
| **Fact Checker** | Verifies claims from the research agents | Tavily MCP |
| **Synthesizer** | Combines all findings into a structured research brief | Groq LLM |

## Content Agents

| Agent | Role |
|-------|------|
| **Strategist** | Analyzes the research brief and produces a strategy document (post type, hook style, CTA, tone) |
| **Copywriter** | Writes the initial draft based on the strategy |
| **Editor** | Scores the draft on hook quality, authenticity, and value — approves or requests revision |
| **Optimizer** | Produces the final post with hook variants, hashtags, and formatted output |

## Project Structure

```
linkedin-content-engine/
├── main.py                        # Entry point
├── pyproject.toml                 # Project metadata & dependencies
├── requirements.txt               # Dependency list
│
├── pipeline/
│   ├── orchestrator.py            # Runs research → content pipeline
│   └── prompt_parser.py           # Extracts GitHub URLs from user input
│
├── research_agent/
│   ├── graph.py                   # LangGraph state machine
│   ├── state.py                   # ResearchState definition
│   ├── agents/                    # Agent implementations
│   ├── schemas/                   # Pydantic output schemas
│   └── prompts/                   # System prompts
│
├── content_agent/
│   ├── agent.py                   # Root agent (SequentialAgent)
│   ├── agents/                    # Agent implementations
│   ├── schemas/                   # Pydantic output schemas
│   └── instruction/              # Agent instructions
│
├── shared/
│   ├── config.py                  # Environment variable loader
│   └── logger.py                  # Logging configuration
│
└── tests/                         # Test suite
```

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js (for MCP servers via `npx`)
- API keys (see below)

### Installation

```bash
git clone https://github.com/your-username/linkedin-content-engine.git
cd linkedin-content-engine

python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# .venv\Scripts\activate    # Windows

pip install -e .
```

### Environment Variables

Create a `.env` file in the project root with the following keys:

```env
# GitHub Analyser
RA_GA_GROQ_API_KEY=your_groq_api_key
RA_GA_GITHUB_API_KEY=your_github_api_key

# News Researcher
RA_NR_GROQ_API_KEY=your_groq_api_key
RA_NR_SERPER_API_KEY=your_serper_api_key

# Trend Analyser
RA_TA_GROQ_API_KEY=your_groq_api_key
RA_TA_EXA_API_KEY=your_exa_api_key

# Fact Checker
RA_FC_GROQ_API_KEY=your_groq_api_key
RA_FC_TAVILY_API_KEY=your_tavily_api_key

# Synthesizer
RA_SY_GROQ_API_KEY=your_groq_api_key

# Supervisor
RA_SU_GROQ_API_KEY=your_groq_api_key
```

> You can use the same Groq API key for all `*_GROQ_API_KEY` variables, or separate keys for rate-limit isolation.

### Usage

```bash
# With a topic prompt
python main.py "Write a post about the rise of AI agents in developer tooling"

# With a GitHub repo
python main.py "Showcase this project https://github.com/owner/repo"

# Interactive mode
python main.py
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Research orchestration | [LangGraph](https://github.com/langchain-ai/langgraph) |
| Content generation | [Google ADK](https://google.github.io/adk-docs/) |
| LLM provider | [Groq](https://groq.com/) |
| Data validation | [Pydantic](https://docs.pydantic.dev/) |
| External search | Google Serper, Exa, Tavily, DuckDuckGo |
| Tool integration | [MCP](https://modelcontextprotocol.io/) (GitHub, Tavily, Exa servers) |

## License

This project is provided as-is for educational and personal use.
