import json

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq

from research_agent.prompts.synthesizer_prompt import SYSTEM_PROMPT
from research_agent.schemas.research_brief_schema import ResearchBrief
from research_agent.state import ResearchState
from shared.config import config
from shared.logger import get_logger

logger = get_logger(__name__)


def _build_research_context(state: ResearchState) -> str:
    """Assemble all agent outputs into a single context string for the Synthesizer LLM."""
    sections: list[str] = []

    sections.append(f"## Original Request\n{state['request']}")

    sections.append(f"## Post Type\n{state['post_type']}")

    project_analysis = state.get("GA_project_analysis")
    if project_analysis:
        sections.append(
            f"## GitHub Project Analysis\n{json.dumps(project_analysis, indent=2)}"
        )

    news_findings = state.get("NR_news_findings")
    if news_findings:
        filtered = {k: v for k, v in news_findings.items() if k != "search_queries_used"}
        sections.append(
            f"## News Researcher Findings\n{json.dumps(filtered, indent=2)}"
        )

    trend_data = state.get("TA_trend_data")
    if trend_data:
        filtered = {k: v for k, v in trend_data.items() if k != "search_queries_used"}
        sections.append(f"## Trend Analyzer Data\n{json.dumps(filtered, indent=2)}")

    fact_check = state.get("FC_fact_check_results")
    if fact_check:
        filtered = {k: v for k, v in fact_check.items() if k != "search_queries_used"}
        sections.append(f"## Fact-Check Results\n{json.dumps(filtered, indent=2)}")

    return "\n\n".join(sections)


async def synthesizer_agent(state: ResearchState) -> dict:
    logger.info("Synthesizer Agent Started")

    research_context = _build_research_context(state)

    model = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.3,
        api_key=config.RA_SY_GROQ_API_KEY,
        max_tokens=4096,
    )

    structured_model = model.with_structured_output(ResearchBrief)

    result = await structured_model.ainvoke(
        [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(
                content=(
                    "Synthesize the following research into a cohesive "
                    "research brief for a LinkedIn post:\n\n"
                    f"{research_context}"
                )
            ),
        ]
    )

    logger.info(
        "Synthesizer Agent Completed — key_points: %d, hooks: %d, evidence: %d",
        len(result.key_points),
        len(result.hook_suggestions),
        len(result.supporting_evidence),
    )

    return {"research_brief": result.model_dump()}
