import asyncio

from research_agent.agents.github_analyser_agent import github_analyzer_agent
from research_agent.state import ResearchState


async def main() -> None:
    state: ResearchState = {
        "request": "Analyze this repo",
        "GA_repo_url": "https://github.com/tssarathi/ai-anime-recommender",
        "GA_project_analysis": None,
    }

    await github_analyzer_agent(state)


if __name__ == "__main__":
    asyncio.run(main())
