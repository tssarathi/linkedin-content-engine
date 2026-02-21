from typing import TypedDict

from research_agent.schemas.github_analyser_schema import ProjectAnalysis
from research_agent.schemas.news_researcher_schema import NewsFindings


class ResearchState(TypedDict):
    # -- Orchestrator Input --
    request: str

    # -- GitHub Analyzer Input--
    GA_repo_url: str | None

    # -- GitHub Analyzer Output--
    GA_project_analysis: ProjectAnalysis | None

    # -- News Researcher Input--
    buzzwords: list[str] | None
    NR_post_type: str | None

    # -- News Researcher Output --
    NR_news_findings: NewsFindings | None
