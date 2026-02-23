from typing import Literal

from pydantic import BaseModel, Field


class StrategyDocument(BaseModel):
    """Strategy document produced by the Strategist for the Copywriter."""

    post_type: Literal[
        "project_showcase",
        "ai_news_commentary",
        "tutorial_build_log",
        "hot_take",
        "weekly_roundup",
    ] = Field(
        description="The post format that best fits the research brief"
    )
    narrative_angle: str = Field(
        description="The specific angle or framing for this post, 1-2 sentences"
    )
    hook_style: Literal[
        "question",
        "bold_claim",
        "relatable_statement",
        "surprising_stat",
        "personal_story",
    ] = Field(
        description="The hook style to use for the opening line"
    )
    target_audience: str = Field(
        description="Specific audience for this post, e.g. 'AI engineers building production agents'"
    )
    cta_type: Literal[
        "follow_for_more",
        "comment_with_opinion",
        "share_if_useful",
        "link_in_comments",
        "ask_a_question",
    ] = Field(
        description="The call-to-action type for the post ending"
    )
    tone_notes: str = Field(
        description="2-3 sentences describing voice, energy level, and specific language to use or avoid"
    )
