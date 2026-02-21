from pydantic import BaseModel, Field


class ProjectAnalysis(BaseModel):
    """Structured output of a GitHub analyser agent."""

    summary: str = Field(
        description="2-3 sentences summarizing what the project does and why it is interesting"
    )
    tech_stack: list[str] = Field(
        description="List of technologies, languages, and frameworks used in the project"
    )
    recent_activity: str = Field(
        description="One-line summary of recent commit activity"
    )
    key_features: list[str] = Field(
        description="Up to 5 key features or capabilities of the project"
    )
