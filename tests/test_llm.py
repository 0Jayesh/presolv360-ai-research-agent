from app.llm import generate_research_dimensions


def test_generate_exactly_10_dimensions():
    result = generate_research_dimensions(
        "The impact of AI on jobs and employment"
    )

    assert len(result.dimensions) == 10

    for dimension in result.dimensions:
        assert dimension.strip()