import json

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from research_agent.prompts.supervisor_prompt import SYSTEM_PROMPT
from research_agent.schemas.supervisor_schema import SupervisorOutput
from research_agent.state import ResearchState
from shared.config import config
from shared.logger import get_logger

logger = get_logger(__name__)


def _build_supervisor_context(state: ResearchState) -> str:
    """Build context string for the Supervisor LLM from request and optional GitHub analysis."""
    sections: list[str] = []

    sections.append(f"## User Request\n{state['request']}")

    project_analysis = state.get("GA_project_analysis")
    if project_analysis:
        sections.append(
            f"## GitHub Project Analysis (from GitHub Analyzer)\n"
            f"{json.dumps(project_analysis, indent=2)}"
        )
    else:
        sections.append(
            "## GitHub Project Analysis\n"
            "No GitHub repository was provided. Derive buzzwords and "
            "project_context from the user's request alone."
        )

    return "\n\n".join(sections)


async def supervisor_agent(state: ResearchState) -> dict:
    """Run the Supervisor: read state, call LLM with structured output, return routing decisions."""
    logger.info("Supervisor Agent started — distributing context")

    context = _build_supervisor_context(state)

    model = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        api_key=config.OPENAI_API_KEY,
    )

    structured_model = model.with_structured_output(SupervisorOutput)

    result = await structured_model.ainvoke(
        [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(
                content=(
                    "Analyze the following and produce routing context "
                    "for the downstream research agents:\n\n"
                    f"{context}"
                )
            ),
        ]
    )

    logger.info(
        "Supervisor completed — post_type=%s, buzzwords=%s",
        result.post_type,
        result.buzzwords,
    )

    return result.model_dump()
