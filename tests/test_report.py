from app.report import render_markdown_report
from app.schemas import (
    ClaimEvidence,
    ComparisonItem,
    ComparisonResult,
)


def test_render_markdown_report():

    claim = ClaimEvidence(
        dimension="Test dimension",
        claim="AI changes employment patterns.",
        evidence="Example supporting evidence.",
        source="https://example.com",
        citation="Section 1",
    )

    comparisons = [
        ComparisonItem(
            dimension=f"Dimension {i}",
            consensus=[claim] if i == 0 else [],
            contradictions=[],
            outliers=[],
            gap="",
        )
        for i in range(10)
    ]

    result = ComparisonResult(
        topic="AI and employment",
        comparisons=comparisons,
    )

    report = render_markdown_report(result)

    assert "# Research Brief: AI and employment" in report
    assert "## Executive Summary" in report
    assert "## Findings by Dimension" in report
    assert "### Dimension 0" in report
    assert "#### Consensus" in report
    assert "AI changes employment patterns." in report
    assert "https://example.com" in report
    assert report.count("### Dimension") == 10