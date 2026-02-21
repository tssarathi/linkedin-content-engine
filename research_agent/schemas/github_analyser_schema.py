from typing_extensions import TypedDict


class ProjectAnalysis(TypedDict):
    """Structured output of a GitHub analyser agent."""

    """2-3 sentences summarizing the project"""
    summary: str

    """Technologies used"""
    tech_stack: list[str]

    """One-line summary of recent commit activity"""
    recent_activity: str

    """Key features (max 5)"""
    key_features: list[str]
