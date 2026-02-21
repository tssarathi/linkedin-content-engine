from typing import Literal

from pydantic import BaseModel, Field


class SupervisorOutput(BaseModel):
    """The Supervisor's structured output — routing decisions and context,
    not research content.

    Every field in this schema corresponds to a field in ResearchState.
    When LangGraph merges the Supervisor's return dict into state, these
    values flow directly into the state without any wrapping or mapping.
    This is intentional: the Supervisor's job IS to set state, so its
    schema IS the state mutation.
    """

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
        description="5-10 precise keywords optimized for DuckDuckGo's lexical search. "
        "These must be specific terms that appear literally in web pages: "
        "framework names ('LangGraph'), protocol names ('MCP'), "
        "company names ('Anthropic'), versioned terms ('GPT-4o'). "
        "Order by specificity — most specific first. "
        "NEVER include generic terms like 'technology' or 'AI' alone — "
        "they return noise in keyword search"
    )
    project_context: str = Field(
        description="A 2-4 sentence natural language summary optimized for "
        "Exa's semantic/neural search. Describe the conceptual space: "
        "what the topic is about, how pieces connect, why it matters now. "
        "Write as if explaining to a knowledgeable colleague, not as a "
        "keyword list. Exa matches meaning, not words — rich descriptions "
        "outperform terse ones"
    )
