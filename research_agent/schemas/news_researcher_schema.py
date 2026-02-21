from pydantic import BaseModel, Field


class NewsItem(BaseModel):
    """Represents a news article found by the agent."""

    title: str = Field(description="The main headline or topic of the article")
    url: str = Field(description="The website link where the article is published")
    summary: str = Field(description="A brief summary of the article (2-3 sentences)")
    relevance: str = Field(
        description="Explanation of why this article is relevant to the research"
    )


class NewsFindings(BaseModel):
    """Represents the structured results from the news researcher."""

    news_items: list[NewsItem] = Field(
        description="List of news items discovered during research"
    )
    search_queries_used: list[str] = Field(
        description="Search queries that were issued to find the news"
    )
    topic_summary: str = Field(
        description="Short, high-level summary of the news topic landscape"
    )
