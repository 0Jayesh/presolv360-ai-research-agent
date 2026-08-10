# NOTES

## Overall approach

I decomposed the problem into four explicit stages rather than using a single large summarization prompt:

1. Generate exactly 10 research dimensions for the topic.
2. Fetch and clean each source.
3. Extract one structured claim/evidence/citation record per dimension for every source, leaving fields empty when a source does not address a dimension.
4. Compare the extracted evidence across sources to identify consensus, contradictions, outliers, and gaps, then render the result as a Markdown research brief.

This structure makes the cross-source reasoning traceable and reduces the chance that the final comparison invents unsupported claims.

## Tradeoffs

Given the two-hour build budget, I chose a sequential LangChain pipeline with Gemini structured outputs and Pydantic validation. I focused on explicit intermediate representations and evidence preservation rather than adding infrastructure such as databases, authentication, or a multi-agent framework.

## Production improvements

For a production version, I would add:

* provider fallback and exponential backoff for rate limits
* asynchronous source fetching
* persistent caching of fetched content and LLM outputs
* stronger observability and structured logging
* mocked LLM responses in unit tests to avoid consuming API quota
* richer citation normalization and source metadata
* evaluation datasets for contradiction and outlier classification
