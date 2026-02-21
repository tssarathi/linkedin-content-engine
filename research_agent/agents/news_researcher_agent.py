from langchain.agents import create_agent
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_groq import ChatGroq

from research_agent.prompts.news_researcher_prompt import SYSTEM_PROMPT
from research_agent.schemas.news_researcher_schema import NewsFindings
from research_agent.state import ResearchState
from shared.config import config
from shared.logger import get_logger

logger = get_logger(__name__)

search = DuckDuckGoSearchResults()


async def news_researcher_Agent(state: ResearchState) -> None:
    logger.info("News Researcher Agent Started")

    request = state["request"]
    post_type = state["post_type"]
    buzzwords = state["buzzwords"]

    tools = [search]

    logger.debug("Tools: %s", [t.name for t in tools])

    model = ChatGroq(
        model="qwen/qwen3-32b",
        temperature=0,
        api_key=config.RA_NR_GROQ_API_KEY,
        max_tokens=8192,
    )

    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
        name="news_researcher",
        response_format=NewsFindings,
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
    logger.info(
        "News Researcher Agent Completed. Found %d articles",
        len(findings.news_items),
    )

    return findings.model_dump()
