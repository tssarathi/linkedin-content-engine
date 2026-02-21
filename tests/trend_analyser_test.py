import asyncio
import pprint as pp

from research_agent.agents.trend_analyser_agent import trend_analyser_agent
from research_agent.state import ResearchState


async def main() -> None:
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
    pp.pprint(trend_data)


if __name__ == "__main__":
    asyncio.run(main())
