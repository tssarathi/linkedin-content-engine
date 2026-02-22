import json

from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from langchain_groq import ChatGroq
from langchain_mcp_adapters.client import MultiServerMCPClient

from research_agent.prompts.fact_checker_prompt import SYSTEM_PROMPT
from research_agent.schemas.fact_checker_schema import FactCheckResults
from research_agent.state import ResearchState
from shared.config import config
from shared.logger import get_logger

logger = get_logger(__name__)

ALLOWED_TOOLS = {"tavily-search"}


def _build_claims_message(state: ResearchState) -> str:
    """Serialize research findings into a message the LLM can extract claims from."""
    sections = []

    news_findings = state.get("NR_news_findings")
    if news_findings:
        sections.append(
            "## News Researcher Findings\n"
            f"{json.dumps(news_findings, indent=2)}"
        )

    trend_data = state.get("TA_trend_data")
    if trend_data:
        sections.append(
            "## Trend Analyzer Findings\n"
            f"{json.dumps(trend_data, indent=2)}"
        )

    return "\n\n".join(sections)


async def fact_checker_agent(state: ResearchState) -> dict:
    logger.info("Fact Checker Agent Started")

    claims_message = _build_claims_message(state)

    if not claims_message:
        logger.warning("No research findings to verify — skipping fact check")
        return FactCheckResults(
            claim_verifications=[],
            search_queries_used=[],
            summary="No research findings were provided to verify.",
        ).model_dump()

    mcp_servers = {
        "tavily": {
            "command": "npx",
            "args": ["-y", "tavily-mcp@latest"],
            "env": {"TAVILY_API_KEY": config.RA_FC_TAVILY_API_KEY},
            "transport": "stdio",
        }
    }

    client = MultiServerMCPClient(mcp_servers)

    all_tools = await client.get_tools()
    tools = [t for t in all_tools if t.name in ALLOWED_TOOLS]

    logger.debug(
        "Using %d/%d Tavily MCP tools: %s",
        len(tools),
        len(all_tools),
        [t.name for t in tools],
    )

    model = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        api_key=config.RA_FC_GROQ_API_KEY,
        max_tokens=4096,
    )

    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
        name="fact_checker",
        response_format=ToolStrategy(FactCheckResults),
    )

    result = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": (
                        "Verify the factual claims in these research findings:\n\n"
                        f"{claims_message}\n\n"
                        "Extract the most important verifiable claims and "
                        "check each one against independent sources."
                    ),
                }
            ]
        }
    )

    fact_check_results = result["structured_response"]
    logger.debug("Search queries used: %s", fact_check_results.search_queries_used)
    verified = sum(
        1 for c in fact_check_results.claim_verifications if c.status == "verified"
    )
    total = len(fact_check_results.claim_verifications)
    logger.info(
        "Fact Checker Agent Completed. %d/%d claims verified", verified, total
    )

    return fact_check_results.model_dump()
