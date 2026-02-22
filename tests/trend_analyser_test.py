import asyncio

from research_agent.agents.trend_analyser_agent import trend_analyser_agent
from research_agent.state import ResearchState


async def test_trend_analyser() -> None:
    state: ResearchState = {
        "request": "AI agents and multi-agent systems using LangGraph",
        "project_context": (
            "A multi-agent LinkedIn content engine that orchestrates research "
            "agents via LangGraph, with MCP for tool integration and A2A protocol "
            "for inter-system communication. Tech stack: Python, LangGraph, "
            "Google ADK, FastAPI, Pydantic."
        ),
    }

    trend_data = await trend_analyser_agent(state)

    ta = trend_data.get("TA_trend_data")
    assert ta is not None, "TA_trend_data should not be None"
    assert len(ta["trending_topics"]) >= 1, "should have at least 1 trending topic"
    assert len(ta["recommended_hashtags"]) >= 1, "should have at least 1 hashtag"
    print("PASS: Trend Analyser")


async def main() -> None:
    await test_trend_analyser()
    print("ALL TESTS PASSED")


if __name__ == "__main__":
    asyncio.run(main())
