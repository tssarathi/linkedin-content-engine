from typing import TypedDict

from research_agent.schemas.fact_checker_schema import FactCheckResults
from research_agent.schemas.github_analyser_schema import ProjectAnalysis
from research_agent.schemas.news_researcher_schema import NewsFindings
from research_agent.schemas.trend_analyser_schema import TrendData


class ResearchState(TypedDict):
    # -- Orchestrator Input --
    request: str
    GA_repo_url: str | None

    # -- GitHub Analyzer Output --
    GA_project_analysis: ProjectAnalysis | None

    # -- Supervisor Output (context for downstream agents) --
    post_type: str
    buzzwords: list[str]
    project_context: str

    # -- News Researcher Output --
    NR_news_findings: NewsFindings | None

    # -- Trend Analyser Output --
    TA_trend_data: TrendData | None

    # -- Fact Checker Output --
    FC_fact_check_results: FactCheckResults | None
