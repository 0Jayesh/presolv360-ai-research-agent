from typing import List
from pydantic import BaseModel, Field, field_validator


# ---------- Stage 0: Research dimensions ----------

class ResearchDimensions(BaseModel):
    dimensions: List[str] = Field(
        ...,
        min_length=10,
        max_length=10,
        description="Exactly 10 important comparison dimensions for the research topic."
    )

    @field_validator("dimensions")
    @classmethod
    def validate_dimensions(cls, value: List[str]) -> List[str]:
        cleaned = [item.strip() for item in value]

        if len(cleaned) != 10:
            raise ValueError("Exactly 10 research dimensions are required.")

        if any(not item for item in cleaned):
            raise ValueError("Research dimensions cannot be empty.")

        if len(set(item.lower() for item in cleaned)) != 10:
            raise ValueError("Research dimensions must be unique.")

        return cleaned


# ---------- Stage 1: Per-source extraction ----------

class ClaimEvidence(BaseModel):
    dimension: str = Field(
        ...,
        description="One of the 10 predefined research dimensions."
    )
    claim: str = Field(
        "",
        description=(
            "One atomic, topic-relevant claim explicitly supported by the source. "
            "Empty string if the source does not address the dimension."
        )
    )
    evidence: str = Field(
        "",
        description=(
            "Relevant passage or evidence from the source supporting the claim. "
            "Empty string when there is no claim."
        )
    )
    source: str = Field(
        "",
        description="Source URL. Empty string when there is no claim."
    )
    citation: str = Field(
        "",
        description=(
            "Location/reference supporting the claim, such as URL, section, "
            "heading, or paragraph reference. Empty string when there is no claim."
        )
    )

class SourceClaims(BaseModel):
    source_url: str
    dimensions: List[ClaimEvidence] = Field(
        ...,
        min_length=10,
        max_length=10,
        description="Exactly one entry for each of the 10 research dimensions."
    )

    @field_validator("dimensions")
    @classmethod
    def validate_dimensions(cls, value: List[ClaimEvidence]) -> List[ClaimEvidence]:
        if len(value) != 10:
            raise ValueError(
                "Every source must contain exactly 10 dimension entries."
            )
        return value


# ---------- Stage 2: Cross-source comparison ----------

class ComparisonItem(BaseModel):
    dimension: str
    consensus: List[ClaimEvidence] = Field(default_factory=list)
    contradictions: List[ClaimEvidence] = Field(default_factory=list)
    outliers: List[ClaimEvidence] = Field(default_factory=list)
    gap: str = ""


class ComparisonResult(BaseModel):
    topic: str
    comparisons: List[ComparisonItem] = Field(
        ...,
        min_length=10,
        max_length=10
    )

    @field_validator("comparisons")
    @classmethod
    def validate_comparisons(
        cls, value: List[ComparisonItem]
    ) -> List[ComparisonItem]:
        if len(value) != 10:
            raise ValueError(
                "Comparison result must contain exactly 10 dimensions."
            )
        return value


# ---------- Stage 3: Final brief ----------

class ResearchBrief(BaseModel):
    topic: str
    executive_summary: str
    consensus: List[str] = Field(default_factory=list)
    contradictions: List[str] = Field(default_factory=list)
    outliers: List[str] = Field(default_factory=list)
    gaps: List[str] = Field(default_factory=list)
    sources: List[str] = Field(default_factory=list)