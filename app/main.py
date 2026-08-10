from app.pipeline import run_research


URLS = [
    "https://insights.som.yale.edu/insights/the-real-job-destruction-from-ai-is-hitting-before-careers-can-start",
    "https://www.library.hbs.edu/working-knowledge/enhance-or-eliminate-how-ai-will-likely-change-these-jobs",
    "https://gloat.com/blog/ai-labor-market/",
    "https://www.brookings.edu/articles/measuring-us-workers-capacity-to-adapt-to-ai-driven-job-displacement/",
    "https://www.jpmorgan.com/insights/global-research/artificial-intelligence/ai-impact-job-growth",
]


if __name__ == "__main__":

    topic = "The impact of AI on jobs and employment"

    dimensions, sources, comparison = run_research(
        topic=topic,
        urls=URLS,
    )

    print("\n=== RESEARCH COMPLETE ===")
    print(f"Sources processed: {len(sources)}")
    print(f"Dimensions: {len(dimensions)}")

    for item in comparison.comparisons:
        print(f"\n## {item.dimension}")

        if item.consensus:
            print("Consensus:", len(item.consensus))

        if item.contradictions:
            print("Contradictions:", len(item.contradictions))

        if item.outliers:
            print("Outliers:", len(item.outliers))

        if item.gap:
            print("Gap:", item.gap)