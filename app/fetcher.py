import time
from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup


@dataclass
class FetchedSource:
    url: str
    title: str
    content: str
    success: bool
    error: str = ""


def fetch_source(
    url: str,
    timeout: int = 15,
    max_retries: int = 2,
) -> FetchedSource:

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 Chrome/131 Safari/537.36"
        )
    }

    last_error = ""

    for attempt in range(max_retries + 1):
        try:
            response = requests.get(
                url,
                headers=headers,
                timeout=timeout,
            )

            response.raise_for_status()

            soup = BeautifulSoup(response.text, "lxml")

            # Remove non-content elements.
            for element in soup(
                ["script", "style", "noscript", "svg", "nav", "footer"]
            ):
                element.decompose()

            title = soup.title.get_text(strip=True) if soup.title else ""

            content = soup.get_text(
                separator="\n",
                strip=True,
            )

            if not content:
                raise ValueError("Page returned empty content.")

            return FetchedSource(
                url=url,
                title=title,
                content=content,
                success=True,
            )

        except Exception as exc:
            last_error = str(exc)

            if attempt < max_retries:
                time.sleep(1)

    return FetchedSource(
        url=url,
        title="",
        content="",
        success=False,
        error=last_error,
    )