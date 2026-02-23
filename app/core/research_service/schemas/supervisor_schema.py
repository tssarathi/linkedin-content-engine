from typing import Literal

from pydantic import BaseModel, Field


class SupervisorOutput(BaseModel):
    """Routing decisions and context distributed to downstream research agents."""

    post_type: Literal[
        "project_showcase",
        "ai_news",
        "hot_take",
        "tutorial",
        "industry_insight",
    ] = Field(
        description="The type of LinkedIn post to create. "
        "'project_showcase' when the user has a GitHub repo to highlight, "
        "'ai_news' for recent developments or announcements, "
        "'hot_take' for opinions or contrarian views, "
        "'tutorial' for how-to or educational content, "
        "'industry_insight' for trend analysis or market commentary"
    )
    buzzwords: list[str] = Field(
        description="5-10 precise keywords optimized for keyword search. "
        "ONLY use terms that appear EXPLICITLY in the GitHub analysis or user request — "
        "never infer, guess, or add technologies not present in the source data. "
        "Examples: framework names from the actual tech_stack, "
        "domain terms from the project summary, "
        "tool/library names the README explicitly mentions. "
        "Order by specificity — most specific first. "
        "NEVER include generic terms like 'technology' alone — "
        "they return noise in keyword search."
    )
    project_context: str = Field(
        description="A 2-4 sentence natural language summary optimized for "
        "Exa's semantic/neural search. Describe the conceptual space: "
        "what the topic is about, how pieces connect, why it matters now. "
        "Write as if explaining to a knowledgeable colleague, not as a "
        "keyword list. Exa matches meaning, not words — rich descriptions "
        "outperform terse ones"
    )
