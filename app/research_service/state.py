from typing import TypedDict

from app.research_service.schemas.fact_checker_schema import FactCheckResults
from app.research_service.schemas.github_analyser_schema import ProjectAnalysis
from app.research_service.schemas.news_researcher_schema import NewsFindings
from app.research_service.schemas.research_brief_schema import ResearchBrief
from app.research_service.schemas.trend_analyser_schema import TrendData


class ResearchState(TypedDict):
    # -- Orchestrator Input --
    request: str

    # -- GitHub Analyzer Input --
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

    # -- Synthesizer Output --
    research_brief: ResearchBrief | None
