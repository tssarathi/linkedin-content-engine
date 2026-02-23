import json

from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient

from app.research_service.prompts.fact_checker_prompt import SYSTEM_PROMPT
from app.research_service.schemas.fact_checker_schema import FactCheckResults
from app.research_service.state import ResearchState
from app.config.config import config
from app.utilities.logger import get_logger

logger = get_logger(__name__)

ALLOWED_TOOLS = {"tavily_search"}


def _build_claims_message(state: ResearchState) -> str:
    """Serialize research findings into a message the LLM can extract claims from."""
    sections = []

    news_findings = state.get("NR_news_findings")
    if news_findings:
        sections.append(
            f"## News Researcher Findings\n{json.dumps(news_findings, indent=2)}"
        )

    trend_data = state.get("TA_trend_data")
    if trend_data:
        sections.append(
            f"## Trend Analyzer Findings\n{json.dumps(trend_data, indent=2)}"
        )

    return "\n\n".join(sections)


async def fact_checker_agent(state: ResearchState) -> dict:
    logger.info("Fact Checker Agent Started")

    claims_message = _build_claims_message(state)

    mcp_servers = {
        "tavily": {
            "command": "npx",
            "args": ["-y", "tavily-mcp@latest"],
            "env": {"TAVILY_API_KEY": config.RS_FC_TAVILY_API_KEY},
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
    verified = sum(
        1 for c in fact_check_results.claim_verifications if c.status == "verified"
    )
    total = len(fact_check_results.claim_verifications)
    logger.info("Fact Checker Agent Completed. %d/%d claims verified", verified, total)

    return {"FC_fact_check_results": fact_check_results.model_dump()}
