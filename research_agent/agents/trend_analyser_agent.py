from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient

from research_agent.prompts.trend_analyser_prompt import SYSTEM_PROMPT
from research_agent.schemas.trend_analyser_schema import TrendData
from research_agent.state import ResearchState
from shared.config import config
from shared.logger import get_logger

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
            "env": {"EXA_API_KEY": config.RA_TA_EXA_API_KEY},
            "transport": "stdio",
        }
    }

    client = MultiServerMCPClient(mcp_servers)

    all_tools = await client.get_tools()
    tools = [t for t in all_tools if t.name in ALLOWED_TOOLS]

    if not tools:
        raise RuntimeError(
            f"Exa MCP server returned no usable tools. "
            f"Expected {ALLOWED_TOOLS}, got {[t.name for t in all_tools]}"
        )

    logger.debug(
        "Using %d/%d Exa MCP tools: %s",
        len(tools),
        len(all_tools),
        [t.name for t in tools],
    )

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
    logger.debug("Search queries used: %s", trend_data.search_queries_used)
    logger.info(
        "Trend Analyser Agent Completed. Found %d trending topics",
        len(trend_data.trending_topics),
    )

    return {"TA_trend_data": trend_data.model_dump()}
