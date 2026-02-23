from app.research_service.prompts.supervisor_prompt import SYSTEM_PROMPT as SUPERVISOR_PROMPT
from app.research_service.prompts.github_analyser_prompt import SYSTEM_PROMPT as GITHUB_ANALYSER_PROMPT
from app.research_service.prompts.news_researcher_prompt import SYSTEM_PROMPT as NEWS_RESEARCHER_PROMPT
from app.research_service.prompts.trend_analyser_prompt import SYSTEM_PROMPT as TREND_ANALYSER_PROMPT
from app.research_service.prompts.fact_checker_prompt import SYSTEM_PROMPT as FACT_CHECKER_PROMPT
from app.research_service.prompts.synthesizer_prompt import SYSTEM_PROMPT as SYNTHESIZER_PROMPT

__all__ = [
    "SUPERVISOR_PROMPT",
    "GITHUB_ANALYSER_PROMPT",
    "NEWS_RESEARCHER_PROMPT",
    "TREND_ANALYSER_PROMPT",
    "FACT_CHECKER_PROMPT",
    "SYNTHESIZER_PROMPT",
]
