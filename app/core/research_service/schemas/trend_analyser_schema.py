from pydantic import BaseModel, Field


class TrendingTopic(BaseModel):
    """A single trending topic discovered during research."""

    topic: str = Field(
        description="The trending topic or theme relevant to this project's domain "
        "(e.g., 'R Shiny dashboards', 'geospatial open data', 'AI agent orchestration')"
    )
    description: str = Field(
        description="Why this topic is trending and what makes it relevant right now (2-3 sentences)"
    )
    source_url: str = Field(description="URL where this trend was identified")


class TrendData(BaseModel):
    """Structured output of the trend analyser agent."""

    trending_topics: list[TrendingTopic] = Field(
        description="3-5 topics currently trending in the project's specific domain related to the request"
    )
    recommended_hashtags: list[str] = Field(
        description="5-8 LinkedIn hashtags to maximize reach — must match the project's actual domain. "
        "Mix broad reach hashtags with niche community hashtags relevant to this specific topic, "
        "not generic AI/tech hashtags unless the project is actually about AI/tech."
    )
    content_patterns: list[str] = Field(
        description="3-5 content patterns performing well on LinkedIn right now "
        "(e.g., 'Build-in-public threads', 'Hot takes on new releases', 'Before/after comparisons')"
    )
    engagement_insights: str = Field(
        description="A paragraph summarizing what type of content is getting high engagement "
        "in this topic area and why"
    )
    search_queries_used: list[str] | None = None
