import asyncio

from research_agent.graph import app


async def test_flow_1_with_github_url() -> None:
    """Flow 1: GitHub URL provided → full pipeline including GitHub analysis."""
    state = await app.ainvoke({
        "request": "Write a LinkedIn post about my NaarmWings project",
        "GA_repo_url": "https://github.com/tssarathi/NaarmWings",
    })

    brief = state.get("research_brief")
    assert brief is not None, "research_brief should not be None"
    assert brief["narrative_angle"], "narrative_angle should not be empty"
    assert len(brief["key_points"]) >= 3, "should have at least 3 key points"
    assert len(brief["hook_suggestions"]) >= 2, "should have at least 2 hooks"
    print("PASS: Flow 1 (with GitHub URL)")


async def test_flow_2_without_github_url() -> None:
    """Flow 2: No GitHub URL → news/opinion pipeline only."""
    state = await app.ainvoke({
        "request": "Write a hot take about AI agents replacing traditional software engineering workflows",
        "GA_repo_url": None,
    })

    assert state.get("GA_project_analysis") is None, \
        "GA_project_analysis should be None when no URL is provided"

    brief = state.get("research_brief")
    assert brief is not None, "research_brief should not be None"
    assert brief["narrative_angle"], "narrative_angle should not be empty"
    assert len(brief["key_points"]) >= 3, "should have at least 3 key points"
    print("PASS: Flow 2 (without GitHub URL)")


async def main() -> None:
    await test_flow_1_with_github_url()
    await test_flow_2_without_github_url()
    print("ALL TESTS PASSED")


if __name__ == "__main__":
    asyncio.run(main())
