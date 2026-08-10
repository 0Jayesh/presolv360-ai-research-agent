from app.schemas import ResearchDimensions


def test_exactly_10_dimensions():
    data = ResearchDimensions(
        dimensions=[f"Dimension {i}" for i in range(1, 11)]
    )

    assert len(data.dimensions) == 10