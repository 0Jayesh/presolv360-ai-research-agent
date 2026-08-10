from app.fetcher import fetch_source


def test_fetch_source():
    result = fetch_source(
        "https://example.com",
        timeout=10,
        max_retries=1,
    )

    assert result.success is True
    assert result.content
    assert result.url == "https://example.com"