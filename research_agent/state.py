from typing import TypedDict


class ResearchState(TypedDict):
    # -- Orchestrator Input --
    request: str

    # -- GitHub Analyzer Output--
    GA_repo_url: str | None
    GA_project_analysis: dict | None
