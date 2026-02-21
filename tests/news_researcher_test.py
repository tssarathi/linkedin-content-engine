import asyncio
import pprint as pp

from research_agent.agents.news_researcher_agent import news_researcher_Agent
from research_agent.state import ResearchState


async def main() -> None:
    state: ResearchState = {
        "request": "Search for the latest news on the OpenClaw framework",
        "NR_post_type": "LinkedIn Post",
        "buzzwords": ["AI", "OpenClaw"],
    }

    findings = await news_researcher_Agent(state)
    pp.pprint(findings)


if __name__ == "__main__":
    asyncio.run(main())
