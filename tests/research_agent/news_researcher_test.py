import asyncio

from research_agent.agents.news_researcher_agent import news_researcher_agent
from research_agent.state import ResearchState


async def test_news_researcher() -> None:
    state: ResearchState = {
        "request": "Search for the latest news on the OpenClaw framework",
        "post_type": "LinkedIn Post",
        "buzzwords": ["AI", "OpenClaw"],
    }

    findings = await news_researcher_agent(state)

    nr = findings.get("NR_news_findings")
    assert nr is not None, "NR_news_findings should not be None"
    assert len(nr["news_items"]) >= 1, "should have at least 1 news item"
    assert nr["topic_summary"], "topic_summary should not be empty"
    print("PASS: News Researcher")


async def main() -> None:
    await test_news_researcher()
    print("ALL TESTS PASSED")


if __name__ == "__main__":
    asyncio.run(main())
