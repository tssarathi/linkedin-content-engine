import json

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq

from research_agent.prompts.supervisor_prompt import SYSTEM_PROMPT
from research_agent.schemas.supervisor_schema import SupervisorOutput
from research_agent.state import ResearchState
from shared.config import config
from shared.logger import get_logger

logger = get_logger(__name__)


def _build_supervisor_context(state: ResearchState) -> str:
    """Assemble the information the Supervisor LLM needs to make its decision.

    This is structurally similar to the Synthesizer's _build_research_context,
    but with a crucial difference: the Synthesizer receives ALL agent outputs
    (it runs last). The Supervisor receives only the request and optionally
    the GitHub analysis (it runs early, before the research agents).

    The Supervisor's context is intentionally sparse — it only knows the
    request and what the GitHub Analyzer found. It does NOT see news findings
    or trend data, because those agents haven't run yet. The Supervisor's
    job is to SET UP what those agents will search for.
    """
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
    """Phase 2 of the Supervisor: Context Distribution.

    Phase 1 (routing — "should we run GitHub Analyzer?") is handled by
    a deterministic conditional edge in graph.py, not by this function.
    By the time this function runs, the GitHub Analyzer has already
    completed (if it was needed), and its output is in the state.

    This function reads the available context, calls the LLM to produce
    structured routing decisions, and returns a dict whose keys map
    directly to ResearchState fields.
    """
    logger.info("Supervisor Agent started — distributing context")

    context = _build_supervisor_context(state)

    model = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        api_key=config.RA_SU_GROQ_API_KEY,
        max_tokens=2048,
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
