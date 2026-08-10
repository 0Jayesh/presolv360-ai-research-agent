from app.llm import get_llm
from app.schemas import ComparisonResult


def compare_sources(
    topic: str,
    dimensions: list[str],
    source_claims: list,
) -> ComparisonResult:

    llm = get_llm().with_structured_output(ComparisonResult)

    evidence_text = []

    for source in source_claims:
        evidence_text.append(f"\nSOURCE: {source.source_url}")

        for item in source.dimensions:
            evidence_text.append(
                f"""
DIMENSION: {item.dimension}
CLAIM: {item.claim}
EVIDENCE: {item.evidence}
CITATION: {item.citation}
"""
            )

    all_evidence = "\n".join(evidence_text)

    dimensions_text = "\n".join(
        f"{i + 1}. {dimension}"
        for i, dimension in enumerate(dimensions)
    )

    prompt = f"""
You are the cross-source reasoning stage of a research agent.

TOPIC:
{topic}

FIXED RESEARCH DIMENSIONS:
{dimensions_text}

EVIDENCE EXTRACTED FROM SOURCES:
{all_evidence}

Compare the supplied source evidence across the EXACT 10 dimensions.

STRICT RULES:

1. Return exactly 10 comparison items, one for each dimension.
2. Use ONLY the supplied claims and evidence.
3. Do NOT introduce outside knowledge.
4. Do NOT invent claims, evidence, citations, or sources.
5. Empty claims mean the source did not address that dimension.
6. Never interpret an empty claim as agreement or disagreement.
7. Do not manufacture consensus from absence of evidence.

CLASSIFICATION:

CONSENSUS:
Include claims when multiple independent sources make materially
similar assertions about the dimension.

CONTRADICTION:
Only classify claims as contradictory when they make materially
incompatible assertions about the SAME proposition, with comparable
scope, timeframe, population, and context.

Different estimates, different time periods, different populations,
or different aspects of a topic are NOT automatically contradictions.

OUTLIER:
An outlier must be a substantive finding or claim made by only one
source. Do NOT classify methodological notes, definitions,
limitations, measurement descriptions, or caveats as outliers.

If evidence is insufficient to establish a contradiction or outlier,
leave that category empty.

GAP:
Identify a meaningful aspect of the current research dimension that is
not adequately addressed by ANY of the supplied sources.

Only report a gap when the absence of evidence is clear from the
supplied source claims.

Do NOT introduce a new topic or fact that is outside the current
dimension.

If the sources collectively provide adequate coverage of the dimension,
return an empty string.

Do not invent facts to fill a gap.

IMPORTANT:
Prefer false negatives over false positives. It is better to leave a
potential contradiction or outlier empty than to incorrectly classify it.

Every consensus, contradiction, and outlier item must retain the original
claim, evidence, source, and citation exactly as supplied.
"""

    return llm.invoke(prompt)