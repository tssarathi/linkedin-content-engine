from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from langchain_groq import ChatGroq
from langchain_mcp_adapters.client import MultiServerMCPClient

from research_agent.prompts.github_analyser_prompt import SYSTEM_PROMPT
from research_agent.schemas.github_analyser_schema import ProjectAnalysis
from research_agent.state import ResearchState
from shared.config import config
from shared.logger import get_logger

logger = get_logger(__name__)


async def github_analyser_agent(state: ResearchState) -> dict:
    logger.info("GitHub Analyser Agent Started")

    repo_url = state["GA_repo_url"]
    parts = repo_url.rstrip("/").split("/")
    if len(parts) < 2 or not all(parts[-2:]):
        raise ValueError(f"Invalid GitHub repository URL: {repo_url!r}")
    owner, repo = parts[-2], parts[-1]

    logger.info("Analyzing repository: %s/%s", owner, repo)

    mcp = {
        "github": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-github"],
            "env": {
                "GITHUB_PERSONAL_ACCESS_TOKEN": config.RA_GA_GITHUB_API_KEY,
            },
            "transport": "stdio",
        }
    }

    ALLOWED_TOOLS = {"get_file_contents", "list_commits"}

    client = MultiServerMCPClient(mcp)

    all_tools = await client.get_tools()
    tools = [t for t in all_tools if t.name in ALLOWED_TOOLS]

    logger.debug(
        "Using %d/%d GitHub MCP tools: %s",
        len(tools),
        len(all_tools),
        [t.name for t in tools],
    )

    model = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        api_key=config.RA_GA_GROQ_API_KEY,
        max_tokens=4096,
    )

    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
        name="github_analyser",
        response_format=ToolStrategy(ProjectAnalysis),
    )

    result = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": (
                        f"Analyze this GitHub repository: {repo_url} "
                        f"(owner: {owner}, repo: {repo})"
                    ),
                }
            ]
        }
    )

    analysis = result["structured_response"]
    logger.info("GitHub Analyser Agent Completed")

    return {"GA_project_analysis": analysis.model_dump()}
