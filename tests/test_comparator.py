from app.fetcher import fetch_source
from app.llm import generate_research_dimensions
from app.extractor import extract_claims
from app.comparator import compare_sources


URLS = [
    "https://insights.som.yale.edu/insights/the-real-job-destruction-from-ai-is-hitting-before-careers-can-start",
    "https://www.library.hbs.edu/working-knowledge/enhance-or-eliminate-how-ai-will-likely-change-these-jobs",
    "https://gloat.com/blog/ai-labor-market/",
    "https://www.brookings.edu/articles/measuring-us-workers-capacity-to-adapt-to-ai-driven-job-displacement/",
    "https://www.jpmorgan.com/insights/global-research/artificial-intelligence/ai-impact-job-growth",
]


def test_compare_sources():

    topic = "The impact of AI on jobs and employment"

    dimensions = generate_research_dimensions(topic)

    extracted_sources = []

    for url in URLS:
        source = fetch_source(url)

        if not source.success:
            print(f"\nFAILED: {url}")
            continue

        result = extract_claims(
            topic=topic,
            dimensions=dimensions.dimensions,
            source_url=source.url,
            source_title=source.title,
            source_content=source.content,
        )

        extracted_sources.append(result)

    assert extracted_sources

    comparison = compare_sources(
        topic=topic,
        dimensions=dimensions.dimensions,
        source_claims=extracted_sources,
    )

    assert len(comparison.comparisons) == 10

    for item in comparison.comparisons:
        print(f"\n### {item.dimension}")

        print("\nCONSENSUS:")
        for claim in item.consensus:
            print("-", claim.claim)

        print("\nCONTRADICTIONS:")
        for claim in item.contradictions:
            print("-", claim.claim)

        print("\nOUTLIERS:")
        for claim in item.outliers:
            print("-", claim.claim)

        print("\nGAP:")
        print(item.gap)