import asyncio

from research_agent.agents.github_analyser_agent import github_analyser_agent
from research_agent.state import ResearchState


async def test_github_analyser() -> None:
    state: ResearchState = {
        "request": "Analyze this repo",
        "GA_repo_url": "https://github.com/tssarathi/NaarmWings",
        "GA_project_analysis": None,
    }

    analysis = await github_analyser_agent(state)

    ga = analysis.get("GA_project_analysis")
    assert ga is not None, "GA_project_analysis should not be None"
    assert ga["summary"], "summary should not be empty"
    assert len(ga["tech_stack"]) >= 1, "tech_stack should not be empty"
    print("PASS: GitHub Analyser")


async def main() -> None:
    await test_github_analyser()
    print("ALL TESTS PASSED")


if __name__ == "__main__":
    asyncio.run(main())
