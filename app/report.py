from app.schemas import ComparisonResult


def render_markdown_report(result: ComparisonResult) -> str:
    lines = [
        f"# Research Brief: {result.topic}",
        "",
        "## Executive Summary",
        "",
    ]

    consensus_count = sum(len(item.consensus) for item in result.comparisons)
    contradiction_count = sum(
        len(item.contradictions) for item in result.comparisons
    )
    outlier_count = sum(len(item.outliers) for item in result.comparisons)
    gap_count = sum(1 for item in result.comparisons if item.gap)

    lines.extend([
        f"- **Dimensions analyzed:** {len(result.comparisons)}",
        f"- **Consensus findings:** {consensus_count}",
        f"- **Contradictory findings:** {contradiction_count}",
        f"- **Outlier findings:** {outlier_count}",
        f"- **Research gaps:** {gap_count}",
        "",
        "## Findings by Dimension",
        "",
    ])

    for item in result.comparisons:
        lines.extend([
            f"### {item.dimension}",
            "",
        ])

        if item.consensus:
            lines.extend(["#### Consensus", ""])
            for claim in item.consensus:
                lines.extend([
                    f"- **{claim.claim}**",
                    f"  - Evidence: {claim.evidence}",
                    f"  - Source: {claim.source}",
                    f"  - Citation: {claim.citation}",
                    "",
                ])

        if item.contradictions:
            lines.extend(["#### Contradictions", ""])
            for claim in item.contradictions:
                lines.extend([
                    f"- **{claim.claim}**",
                    f"  - Evidence: {claim.evidence}",
                    f"  - Source: {claim.source}",
                    f"  - Citation: {claim.citation}",
                    "",
                ])

        if item.outliers:
            lines.extend(["#### Outliers", ""])
            for claim in item.outliers:
                lines.extend([
                    f"- **{claim.claim}**",
                    f"  - Evidence: {claim.evidence}",
                    f"  - Source: {claim.source}",
                    f"  - Citation: {claim.citation}",
                    "",
                ])

        if item.gap:
            lines.extend([
                "#### Gap",
                "",
                item.gap,
                "",
            ])

    lines.extend([
        "## Sources",
        "",
    ])

    sources = set()

    for item in result.comparisons:
        for claims in (
            item.consensus,
            item.contradictions,
            item.outliers,
        ):
            for claim in claims:
                if claim.source:
                    sources.add(claim.source)

    for source in sorted(sources):
        lines.append(f"- {source}")

    lines.append("")

    return "\n".join(lines)