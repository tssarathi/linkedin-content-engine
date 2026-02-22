from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from langchain_community.tools import GoogleSerperRun
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_groq import ChatGroq

from research_agent.prompts.news_researcher_prompt import SYSTEM_PROMPT
from research_agent.schemas.news_researcher_schema import NewsFindings
from research_agent.state import ResearchState
from shared.config import config
from shared.logger import get_logger

logger = get_logger(__name__)


async def news_researcher_agent(state: ResearchState) -> dict:
    logger.info("News Researcher Agent Started")

    request = state["request"]
    post_type = state["post_type"]
    buzzwords = state["buzzwords"]

    search = GoogleSerperRun(
        api_wrapper=GoogleSerperAPIWrapper(
            serper_api_key=config.RA_NR_SERPER_API_KEY,
            type="news",
            k=5,
        )
    )
    tools = [search]

    logger.debug("Tools: %s", [t.name for t in tools])

    model = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        api_key=config.RA_NR_GROQ_API_KEY,
        max_tokens=4096,
    )

    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
        name="news_researcher",
        response_format=ToolStrategy(NewsFindings),
    )

    result = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": (
                        f"Find the latest AI and tech news related to: {request}\n"
                        f"Post type: {post_type}\n"
                        f"Buzzwords: {buzzwords}\n"
                        f"The news should be relevant to the buzzwords and the post type. "
                        f"The news should be from the last 90 days."
                    ),
                }
            ]
        }
    )

    findings = result["structured_response"]
    logger.debug("Search queries used: %s", findings.search_queries_used)
    logger.info(
        "News Researcher Agent Completed. Found %d articles",
        len(findings.news_items),
    )

    return {"NR_news_findings": findings.model_dump()}
