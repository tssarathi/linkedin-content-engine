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
├── main.py                           # Unified launcher: starts backend + frontend together
├── pyproject.toml                    # Project metadata & dependencies (v3.0.0)
├── requirements.txt                  # Flat dependency list
├── Dockerfile                        # Application Docker image (exposes 8000 + 8501)
├── Jenkinsfile                       # CI/CD: SonarQube analysis + ECR build/push
├── .env.example                      # Template for required API keys
│
├── jenkins/
│   └── Dockerfile                    # Custom Jenkins LTS image with Docker-in-Docker
│
├── app/
│   ├── backend/
│   │   └── api.py                    # FastAPI app — POST /request endpoint
│   │
│   ├── frontend/
│   │   └── ui.py                     # Streamlit UI — connects to backend on port 8000
│   │
│   ├── config/
│   │   └── config.py                 # Centralised environment variable loader
│   │
│   ├── utilities/
│   │   ├── logger.py                 # Dual-output logging (DEBUG → file, INFO → console)
│   │   └── prompt_parser.py          # Extracts GitHub URLs from user input
│   │
│   └── core/
│       ├── linkedin_content_engine.py  # Pipeline orchestration (get_post coroutine)
│       ├── research_service/
│       │   ├── graph.py              # LangGraph StateGraph definition
│       │   ├── state.py              # ResearchState TypedDict
│       │   ├── agents/               # Agent implementations
│       │   ├── schemas/              # Pydantic output schemas
│       │   └── prompts/              # System prompts
│       │
│       └── content_service/
│           ├── agent.py              # Root agent (SequentialAgent)
│           ├── agents/               # Agent implementations
│           ├── schemas/              # Pydantic output schemas
│           └── prompts/              # Agent instructions
│
└── interactive/                      # Optional: feature-rich demo mode (not included in Docker image)
    ├── run.py                        # Interactive launcher (backend on 8100, frontend on 8501)
    ├── backend/
    │   ├── api.py                    # Async job API: POST /generate, GET /status/{id}, GET /jobs
    │   ├── engine.py                 # Pipeline runner with per-agent trace + token tracking
    │   ├── job_store.py              # In-memory job/agent state store
    │   └── schemas.py                # JobState, AgentProgress, TraceEvent, TokenUsage
    ├── dashboard/
    │   └── app.py                    # Streamlit dashboard (wide layout, sidebar history, live polling)
    └── frontend/
        └── components.py             # Agent cards, trace viewer, progress bar, output section
```

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js (for MCP servers via `npx`)
- Docker (optional — for containerised deployment)
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

## Usage

### Web Application (Recommended)

The primary way to run the app — starts both the FastAPI backend and Streamlit frontend together:

```bash
python main.py
```

- Backend API: `http://localhost:8000`
- Frontend UI: `http://localhost:8501`
- API Docs (Swagger): `http://localhost:8000/docs`

### Interactive Demo Mode

A feature-rich version with live per-agent progress tracking, token usage, cost breakdown, and a dashboard with job history:

```bash
python interactive/run.py
```

- Backend API: `http://localhost:8100`
- Dashboard: `http://localhost:8501`

**Dashboard features:**
- Real-time progress bar showing agent completion
- Live agent trace view split by Research Service and Content Service
- Per-agent token usage and cost tracking
- Hook variant tabs (Original / Question / Bold Claim / Relatable)
- Editor score breakdown (Hook Strength, Authenticity, Value Density)
- Pipeline metrics summary (total tokens, cost, time)
- Sidebar with job history

### CLI

```bash
# With a topic prompt
python -m app.core.linkedin_content_engine "Write a post about the rise of AI agents in developer tooling"

# With a GitHub repo
python -m app.core.linkedin_content_engine "Showcase this project https://github.com/owner/repo"

# Interactive mode
python -m app.core.linkedin_content_engine
```

## API Reference

### `POST /request`

Generate a LinkedIn post from a prompt.

**Request:**
```json
{
  "prompt": "Write a post about the rise of AI agents in developer tooling"
}
```

**Response:**
```json
{
  "post": "The publish-ready LinkedIn post text..."
}
```

**Error responses:**
| Status | Description |
|--------|-------------|
| `429` | Gemini API rate limit exceeded |
| `500` | Internal server error |

## Docker

### Build

```bash
docker build -t linkedin-content-engine .
```

### Run

```bash
# Pass API keys as environment variables
docker run -p 8000:8000 -p 8501:8501 \
  -e OPENAI_API_KEY=sk-... \
  -e GOOGLE_API_KEY=... \
  -e RS_GA_GITHUB_API_KEY=... \
  -e RS_NR_SERPER_API_KEY=... \
  -e RS_TA_EXA_API_KEY=... \
  -e RS_FC_TAVILY_API_KEY=... \
  linkedin-content-engine

# Or mount a .env file
docker run -p 8000:8000 -p 8501:8501 \
  --env-file .env \
  linkedin-content-engine
```

> **Note:** The Docker image does not include Node.js. MCP-backed agents (GitHub Analyser, Trend Analyser, Fact Checker) require `npx` at runtime and will not function inside the container without adding Node.js to the Dockerfile.

## CI/CD Pipeline

The project includes a Jenkins pipeline (`Jenkinsfile`) with the following stages:

| Stage | Description |
|-------|-------------|
| **Clone** | Checks out `main` from GitHub |
| **SonarQube Analysis** | Runs static code analysis via SonarQube |
| **Build & Push to ECR** | Builds the Docker image and pushes to AWS ECR (`ap-southeast-2`) |

A custom Jenkins image (`jenkins/Dockerfile`) with Docker-in-Docker support is provided for running the pipeline.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Research orchestration | [LangGraph](https://github.com/langchain-ai/langgraph) |
| Content generation | [Google ADK](https://google.github.io/adk-docs/) |
| Research LLM | [OpenAI GPT-4o-mini](https://platform.openai.com/) |
| Content LLM | [Google Gemini 2.5 Flash Lite](https://ai.google.dev/) |
| Backend API | [FastAPI](https://fastapi.tiangolo.com/) + [Uvicorn](https://www.uvicorn.org/) |
| Frontend UI | [Streamlit](https://streamlit.io/) |
| Data validation | [Pydantic](https://docs.pydantic.dev/) |
| External search | Google Serper, Exa, Tavily |
| Tool integration | [MCP](https://modelcontextprotocol.io/) (GitHub, Tavily, Exa servers via `npx`) |
| Containerisation | [Docker](https://www.docker.com/) |
| CI/CD | [Jenkins](https://www.jenkins.io/) + [AWS ECR](https://aws.amazon.com/ecr/) |
| Observability | [Langfuse](https://langfuse.com/) + [OpenInference](https://github.com/Arize-ai/openinference) |

## License

This project is provided as-is for educational and personal use.
