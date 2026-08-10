from app.llm import get_llm
from app.schemas import SourceClaims


def extract_claims(
    topic: str,
    dimensions: list[str],
    source_url: str,
    source_title: str,
    source_content: str,
) -> SourceClaims:

    llm = get_llm().with_structured_output(SourceClaims)

    dimensions_text = "\n".join(
        f"{i + 1}. {dimension}"
        for i, dimension in enumerate(dimensions)
    )

    prompt = f"""
You are extracting evidence from ONE source for a multi-source research task.

RESEARCH TOPIC:
{topic}

FIXED RESEARCH DIMENSIONS:
{dimensions_text}

SOURCE URL:
{source_url}

SOURCE TITLE:
{source_title}

SOURCE CONTENT:
{source_content}

Your task:
For EACH of the exactly 10 dimensions, determine whether this source
actually makes a relevant claim about that dimension.

STRICT RULES:

1. Return exactly 10 dimension entries, in the same order as provided.
2. A claim must be explicitly supported by the source content.
3. Do NOT use outside knowledge.
4. Do NOT infer a claim merely because the dimension is relevant.
5. Do NOT make predictions or assumptions.
6. If the source does not meaningfully address a dimension, return:
   claim = ""
   evidence = ""
   source = ""
   citation = ""
7. Keep claims atomic: one meaningful assertion per dimension.
8. Evidence must come directly from the supplied source content.
9. The source field must contain the supplied source URL.
10. Citation should identify the relevant location in the source as precisely
    as possible using the available heading, section, paragraph, or URL.
11. Never fabricate a citation.
12. Do not treat absence of discussion as a claim.
13. Preserve uncertainty or qualifications expressed by the source.

The goal is faithful evidence extraction, NOT summarization.
"""

    result = llm.invoke(prompt)

    # Enforce source URL on populated claims.
    for item in result.dimensions:
        if item.claim.strip():
            item.source = source_url

    result.source_url = source_url

    return result