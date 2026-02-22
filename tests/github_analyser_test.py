import asyncio
from pprint import pprint

from research_agent.agents.github_analyser_agent import github_analyser_agent
from research_agent.state import ResearchState


async def main() -> None:
    state: ResearchState = {
        "request": "Analyze this repo",
        "GA_repo_url": "https://github.com/tssarathi/NaarmWings",
        "GA_project_analysis": None,
    }

    analysis = await github_analyser_agent(state)
    pprint(analysis)


if __name__ == "__main__":
    asyncio.run(main())
