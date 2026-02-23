from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient

from app.research_service.prompts.trend_analyser_prompt import SYSTEM_PROMPT
from app.research_service.schemas.trend_analyser_schema import TrendData
from app.research_service.state import ResearchState
from app.config.config import config
from app.utilities.logger import get_logger

logger = get_logger(__name__)

ALLOWED_TOOLS = {"web_search_exa"}


async def trend_analyser_agent(state: ResearchState) -> dict:
    logger.info("Trend Analyser Agent Started")

    request = state["request"]
    project_context = state.get("project_context") or ""

    mcp_servers = {
        "exa": {
            "command": "npx",
            "args": ["-y", "exa-mcp-server"],
            "env": {"EXA_API_KEY": config.RS_TA_EXA_API_KEY},
            "transport": "stdio",
        }
    }

    client = MultiServerMCPClient(mcp_servers)

    all_tools = await client.get_tools()
    tools = [t for t in all_tools if t.name in ALLOWED_TOOLS]

    model = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        api_key=config.OPENAI_API_KEY,
    )

    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
        name="trend_analyser",
        response_format=ToolStrategy(TrendData),
    )

    context_block = ""
    if project_context:
        context_block = (
            f"\nCONTEXT:\n{project_context}\n"
            f"Use this context to craft semantically rich search queries — "
            f"Exa understands meaning, so describe concepts in natural language "
            f"rather than searching for individual keywords.\n"
        )

    result = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": (
                        f"Find trending topics, content patterns, and hashtags "
                        f"related to: {request}"
                        f"{context_block}\n"
                        f"Focus on what's getting engagement on LinkedIn right now."
                    ),
                }
            ]
        }
    )

    trend_data = result["structured_response"]
    logger.info(
        "Trend Analyser Agent Completed. Found %d trending topics",
        len(trend_data.trending_topics),
    )

    return {"TA_trend_data": trend_data.model_dump()}
