import asyncio

from research_agent.agents.supervisor import supervisor_agent
from research_agent.state import ResearchState


async def test_with_github_analysis() -> None:
    state: ResearchState = {
        "request": "Write a LinkedIn post about my multi-agent content engine project",
        "GA_repo_url": "https://github.com/sarathi/linkedin-content-engine",
        "GA_project_analysis": {
            "summary": (
                "A multi-agent LinkedIn content engine that orchestrates research "
                "agents via LangGraph. It uses MCP for tool integration (GitHub, "
                "Exa, Tavily) and produces structured research briefs that feed "
                "into a content generation service."
            ),
            "tech_stack": ["Python", "LangGraph", "FastAPI", "Pydantic", "Groq"],
            "recent_activity": "Added Fact Checker agent with Tavily MCP verification loop",
            "key_features": [
                "Multi-agent orchestration with LangGraph StateGraph",
                "MCP stdio transport for GitHub, Exa, and Tavily tools",
                "Hybrid search: DuckDuckGo (keyword) + Exa (semantic)",
                "Fact-checking with loop-back for unverified claims",
                "Structured output via Pydantic schemas at every stage",
            ],
        },
    }

    result = await supervisor_agent(state)

    assert result["post_type"] == "project_showcase"
    assert len(result["buzzwords"]) >= 5
    assert len(result["project_context"]) > 50
    print("PASS: Supervisor — with GitHub analysis")


async def test_without_github() -> None:
    state: ResearchState = {
        "request": "Write a hot take about AI agents replacing traditional software",
        "GA_repo_url": None,
        "GA_project_analysis": None,
    }

    result = await supervisor_agent(state)

    assert result["post_type"] == "hot_take"
    assert len(result["buzzwords"]) >= 5
    assert len(result["project_context"]) > 50
    print("PASS: Supervisor — without GitHub URL")


async def test_vague_request() -> None:
    state: ResearchState = {
        "request": "Write me a LinkedIn post about AI",
        "GA_repo_url": None,
        "GA_project_analysis": None,
    }

    result = await supervisor_agent(state)

    assert result["post_type"] in ("ai_news", "industry_insight", "hot_take")
    assert len(result["buzzwords"]) >= 3
    assert len(result["project_context"]) > 20
    print("PASS: Supervisor — vague request")


async def main() -> None:
    await test_with_github_analysis()
    await test_without_github()
    await test_vague_request()
    print("ALL TESTS PASSED")


if __name__ == "__main__":
    asyncio.run(main())
