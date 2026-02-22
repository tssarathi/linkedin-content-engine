from pydantic import BaseModel, Field


class HookVariants(BaseModel):
    question: str = Field(description="Hook variant using a question style")
    bold_claim: str = Field(description="Hook variant using a bold claim style")
    relatable_statement: str = Field(description="Hook variant using a relatable statement style")
    original: str = Field(description="The original hook from the approved draft")


class LinkedInPost(BaseModel):
    """Final publish-ready LinkedIn post produced by the Optimizer."""

    hook_variants: HookVariants = Field(
        description="Three alternative hook variants plus the original"
    )
    body: str = Field(
        description="Complete post body, fully formatted, without hashtags"
    )
    hashtags: list[str] = Field(
        description="3 to 5 hashtags including a mix of broad and niche tags",
        min_length=3,
        max_length=5,
    )
    character_count: int = Field(
        description="Character count of body only, not including the hashtags line"
    )
    publish_ready_post: str = Field(
        description="Complete copy-paste ready post: body + blank line + hashtags on final line"
    )
