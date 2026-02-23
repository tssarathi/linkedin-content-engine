from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from langchain_community.tools import GoogleSerperRun
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_openai import ChatOpenAI

from app.research_service.prompts.news_researcher_prompt import SYSTEM_PROMPT
from app.research_service.schemas.news_researcher_schema import NewsFindings
from app.research_service.state import ResearchState
from app.config.config import config
from app.utilities.logger import get_logger

logger = get_logger(__name__)


async def news_researcher_agent(state: ResearchState) -> dict:
    logger.info("News Researcher Agent Started")

    request = state["request"]
    post_type = state.get("post_type", "")
    buzzwords = state.get("buzzwords", [])

    search = GoogleSerperRun(
        api_wrapper=GoogleSerperAPIWrapper(
            serper_api_key=config.RA_NR_SERPER_API_KEY,
            type="news",
            k=5,
        )
    )
    tools = [search]

    model = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        api_key=config.OPENAI_API_KEY,
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
                        f"Find the latest news relevant to: {request}\n"
                        f"Post type: {post_type}\n"
                        f"Buzzwords: {buzzwords}\n"
                        f"Search for news in the project's actual domain — use the buzzwords "
                        f"to determine what domain this is (e.g., data visualization, "
                        f"geospatial, AI agents, open source). "
                        f"The news should be from the last 90 days."
                    ),
                }
            ]
        }
    )

    findings = result["structured_response"]
    logger.info(
        "News Researcher Agent Completed. Found %d articles",
        len(findings.news_items),
    )

    return {"NR_news_findings": findings.model_dump()}
