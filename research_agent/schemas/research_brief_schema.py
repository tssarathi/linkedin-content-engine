from typing import Literal

from pydantic import BaseModel, Field


class SupportingEvidence(BaseModel):
    """A single piece of evidence backing a key point in the brief."""

    point: str = Field(
        description="A specific factual claim or data point that supports the narrative"
    )
    source_url: str | None = Field(
        description="URL where this evidence was found, or None if derived from project analysis"
    )
    verification_status: Literal[
        "verified", "unverified", "partially_verified"
    ] = Field(
        description="How the Fact Checker rated this evidence. "
        "Use 'verified' for claims confirmed by the Fact Checker, "
        "'unverified' for claims not checked or not confirmed, "
        "'partially_verified' for claims with partial support"
    )


class ResearchBrief(BaseModel):
    """The final output of System 1 — the data contract System 2 consumes via A2A.

    This schema represents a complete, actionable research brief that contains
    everything needed to write a LinkedIn post without any additional research.
    """

    narrative_angle: str = Field(
        description="The ONE compelling story angle that ties all the research together. "
        "This is not a topic — it is a specific, opinionated angle on the topic. "
        "Example: not 'AI agents' but 'Why AI agents are replacing traditional "
        "ETL pipelines, and what that means for data engineers'"
    )
    key_points: list[str] = Field(
        description="3-5 main talking points for the post, ordered by importance. "
        "Each point should be a complete, standalone insight — not a section header"
    )
    supporting_evidence: list[SupportingEvidence] = Field(
        description="Verified facts, statistics, and examples that back up the key points. "
        "Prioritize verified evidence over unverified claims"
    )
    post_type: str = Field(
        description="The content type inherited from the Supervisor "
        "(e.g., 'project_showcase', 'ai_news', 'hot_take')"
    )
    recommended_hashtags: list[str] = Field(
        description="5-8 hashtags curated from trend analysis, "
        "mixing broad reach (#AI) with niche targeting (#LangGraph)"
    )
    content_style_suggestion: str = Field(
        description="A specific content format recommendation based on what is performing "
        "well on LinkedIn right now (e.g., 'Build-in-public narrative with a "
        "before/after structure showing the problem you solved')"
    )
    hook_suggestions: list[str] = Field(
        description="2-3 possible opening hooks for the post. "
        "Each should be a complete first line that creates curiosity or tension"
    )
    target_audience: str = Field(
        description="Who this post speaks to — specific enough to guide tone and vocabulary "
        "(e.g., 'Senior engineers evaluating agent frameworks' not just 'developers')"
    )
    brief_summary: str = Field(
        description="2-3 sentence executive summary of the entire brief. "
        "A reader should understand the angle, key evidence, and recommended "
        "approach from this summary alone"
    )
