from app.llm import generate_research_dimensions
from app.fetcher import fetch_source
from app.extractor import extract_claims
from app.comparator import compare_sources


def run_research(topic: str, urls: list[str]):

    # Stage 0: fixed research framework
    dimensions_result = generate_research_dimensions(topic)
    dimensions = dimensions_result.dimensions

    # Stage 1: fetch + extract each source
    extracted_sources = []

    for url in urls:
        source = fetch_source(url)

        if not source.success:
            print(f"WARNING: Failed to fetch {url}: {source.error}")
            continue

        claims = extract_claims(
            topic=topic,
            dimensions=dimensions,
            source_url=source.url,
            source_title=source.title,
            source_content=source.content,
        )

        extracted_sources.append(claims)

    if not extracted_sources:
        raise RuntimeError("No sources could be successfully processed.")

    # Stage 2: cross-source reasoning
    comparison = compare_sources(
        topic=topic,
        dimensions=dimensions,
        source_claims=extracted_sources,
    )

    return dimensions, extracted_sources, comparison