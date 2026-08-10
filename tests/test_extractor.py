from app.fetcher import fetch_source
from app.llm import generate_research_dimensions
from app.extractor import extract_claims


def test_extract_claims():

    topic = "The impact of AI on jobs and employment"

    dimensions = generate_research_dimensions(topic)

    source = fetch_source(
        "https://insights.som.yale.edu/insights/the-real-job-destruction-from-ai-is-hitting-before-careers-can-start"
    )

    assert source.success is True

    result = extract_claims(
        topic=topic,
        dimensions=dimensions.dimensions,
        source_url=source.url,
        source_title=source.title,
        source_content=source.content,
    )

    assert len(result.dimensions) == 10

    for item in result.dimensions:
        assert item.dimension.strip()

    print("\n\nEXTRACTED CLAIMS:\n")

    for item in result.dimensions:
        print(f"\n[{item.dimension}]")
        print(f"Claim: {item.claim}")
        print(f"Evidence: {item.evidence[:300]}")
        print(f"Citation: {item.citation}")