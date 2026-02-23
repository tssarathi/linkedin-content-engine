from pydantic import BaseModel, Field


class EditorScores(BaseModel):
    hook_strength: int = Field(description="Hook strength score from 1 to 10", ge=1, le=10)
    authenticity: int = Field(description="Authenticity score from 1 to 10", ge=1, le=10)
    value_density: int = Field(description="Value density score from 1 to 10", ge=1, le=10)


class MechanicalChecks(BaseModel):
    character_count: int = Field(description="Actual character count of the post body")
    banned_phrases_found: list[str] = Field(
        description="List of banned phrases found in the draft, empty if none"
    )
    hook_on_line_1: bool = Field(description="Whether the hook appears on line 1 with no preamble")
    no_hashtags: bool = Field(description="Whether the draft is free of hashtags")


class EditorReview(BaseModel):
    """Structured output of the editor agent quality gate."""

    scores: EditorScores = Field(description="Rubric scores for the draft")
    mechanical_checks: MechanicalChecks = Field(description="Mechanical quality checks")
    approved: bool = Field(
        description="True if all scores >= 8 or this is the second review; False otherwise"
    )
    feedback: str = Field(
        description="If approved: brief note on what worked. "
        "If not approved: specific, actionable feedback referencing exact lines or phrases to fix"
    )
