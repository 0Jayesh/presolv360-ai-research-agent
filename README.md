# AI Research-and-Summarize Agent

A lightweight AI-native research agent that analyzes a topic across multiple web sources and produces an evidence-grounded research brief highlighting consensus, contradictions, outliers, and research gaps.

## Architecture

```text
Topic + 3–5 URLs
        │
        ▼
Stage 0: Generate exactly 10 research dimensions
        │
        ▼
Stage 1: Fetch and clean each source
        │
        ▼
Stage 2: Extract structured claims per source
        │
        ▼
Stage 3: Compare claims across sources
        │
        ▼
Markdown Research Brief
```

The pipeline uses LangChain with Gemini structured outputs and Pydantic schemas to keep each stage deterministic and traceable.

## Key Design Decisions

* **Fixed comparison framework:** The model first generates exactly 10 dimensions for the topic. Every source is evaluated against those same dimensions.
* **Structured extraction:** Each source returns one claim/evidence/citation record per dimension. If a source does not address a dimension, the fields are left empty rather than inferred.
* **Grounded comparison:** The comparison stage receives only extracted evidence and is instructed not to introduce outside knowledge or invent citations.
* **High-precision reasoning:** The comparator prefers false negatives over false positives when identifying contradictions and outliers.

## Project Structure

```text
app/
  llm.py          # LLM configuration and dimension generation
  fetcher.py      # Web fetching and HTML cleaning
  extractor.py    # Per-source claim extraction
  comparator.py   # Cross-source reasoning
  report.py       # Markdown report generation
  pipeline.py     # Orchestration
  main.py         # Example end-to-end run

tests/
  test_schemas.py
  test_llm.py
  test_fetcher.py
  test_extractor.py
  test_comparator.py
  test_report.py
```

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file:

```text
GOOGLE_API_KEY=your_gemini_api_key
```

## Run

```bash
python -m app.main
```

The pipeline processes the configured sources and writes:

```text
research_brief.md
```

## Test

```bash
python -m pytest tests -v
```

Current status:

```text
6 passed
```

## Output

The generated research brief contains:

* Executive summary
* Consensus findings
* Contradictions
* Outlier claims
* Research gaps
* Source citations

## Tradeoffs

This implementation intentionally prioritizes clarity and traceability over production-scale complexity. It uses a sequential pipeline and a single LLM provider to fit the exercise's two-hour scope while keeping the reasoning stages explicit and easy to inspect.

For a production deployment, I would add provider fallbacks, persistent caching, asynchronous fetching, observability, and mocked LLM responses for deterministic unit tests.
