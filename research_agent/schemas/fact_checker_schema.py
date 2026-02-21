from typing import Literal

from pydantic import BaseModel, Field


class ClaimVerification(BaseModel):
    """Verification result for a single factual claim."""

    claim: str = Field(
        description="The specific factual claim being verified, quoted from the research findings"
    )
    status: Literal["verified", "unverified", "partially_verified"] = Field(
        description="Whether the claim was confirmed, denied, or only partially supported by independent sources"
    )
    confidence: float = Field(
        description="Confidence in the verification judgment, from 0.0 (no confidence) to 1.0 (fully confident)",
        ge=0.0,
        le=1.0,
    )
    source_url: str | None = Field(
        description="URL of the independent source used to verify or refute this claim, "
        "or None if no relevant source was found"
    )
    reasoning: str = Field(
        description="Explanation of why this verification status was assigned, "
        "including what evidence was found or why verification failed"
    )


class FactCheckResults(BaseModel):
    """Structured output of the fact checker agent."""

    claim_verifications: list[ClaimVerification] = Field(
        description="Verification results for each factual claim extracted from the research findings"
    )
    search_queries_used: list[str] = Field(
        description="The search queries used during the fact-checking process"
    )
    summary: str = Field(
        description="Brief overall summary of the fact-checking results, "
        "noting how many claims were verified, unverified, and any concerns"
    )
