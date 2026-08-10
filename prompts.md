# AI-Assisted Build Prompts

This file contains the key prompts used during the build, selected from
the iterative development conversation. The interaction was intentionally
iterative rather than a single upfront specification.

The prompts below capture the major design decisions, implementation
constraints, and refinements made during development.

## 1. Initial Architecture

### Prompt

I need to build the Presolv360 research-and-summarize agent described
in the assignment. I am considering LangChain because the workflow is
a sequential pipeline rather than a complex state machine.

The agent needs to:
- accept a topic and 3–5 source URLs
- fetch and parse the sources
- extract claims with evidence and citations
- compare claims across sources
- identify consensus, contradictions, outliers and gaps
- produce a structured final brief

Help me reason about the architecture before implementing it.

## 2. Fixed Research Dimensions

### Prompt

Before fetching the sources, I want the LLM to identify exactly 10
dimensions that are useful for comparing this research topic.

The important constraint is that the number must be fixed at exactly 10.
Every source must subsequently be evaluated against the same 10 dimensions.

If a source does not address a dimension, it must return an empty value.
It must not infer or invent something merely to populate the dimension.

Use structured output and validation to enforce this.

## 3. Claim Extraction

### Prompt

For each source, extract one atomic claim for each of the 10 fixed
research dimensions.

Each claim should contain:
- claim
- evidence
- source
- citation

The extraction must be grounded only in the supplied source content.

If the source does not address a dimension, return empty strings rather
than generating a claim.

Use Pydantic structured output so every source has exactly 10 entries.

## 4. Cross-Source Comparison

### Prompt

Now compare the structured claims from all sources across the same 10
dimensions.

Identify:
- consensus: materially similar claims from multiple sources
- contradictions: materially incompatible claims about the same
  proposition
- outliers: substantive claims made by only one source
- gaps: meaningful aspects of a dimension that none of the sources
  adequately address

Use only the supplied claims and evidence.

Do not introduce outside knowledge or invent claims, evidence,
citations, or sources.

Empty claims mean that a source did not address the dimension.

Different estimates, time periods, populations or contexts should not
automatically be treated as contradictions.

Prefer false negatives over false positives.

## 5. Comparator Refinement

### Prompt

The initial comparison can incorrectly classify different estimates or
different contexts as contradictions.

Tighten the comparison rules so that a contradiction requires the same
substantive proposition with comparable scope, timeframe, population and
context.

Also ensure methodological notes, definitions, limitations and caveats
are not classified as substantive outliers.

When evidence is insufficient, leave the category empty.

## 6. Final Report

### Prompt

Convert the structured comparison result into a concise Markdown
research brief suitable for an analyst or PM.

Include:
- executive summary
- findings by dimension
- consensus
- contradictions
- outliers
- gaps
- source citations

Do not generate new research claims during rendering. The renderer
should only present the structured comparison result.

## Build Iteration Notes / Validation

During implementation I iteratively:
- validated the Pydantic schemas
- tested the Gemini structured-output call
- tested source fetching
- tested per-source extraction
- tested cross-source comparison
- refined the comparator after observing overly broad contradiction
  classifications
- added the Markdown report stage
- ran the complete test suite and end-to-end pipeline