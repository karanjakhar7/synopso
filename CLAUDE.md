# Synopso — Claude Code Guide

## What this project does

Synopso is a daily pipeline that scrapes HuggingFace Papers, downloads ArXiv PDFs, summarizes them with any LLM via LiteLLM, and delivers summaries to a Telegram channel.

## Running locally

```bash
uv sync                          # install deps
uv run python -m core.main       # full run
uv run python -m core.main --test  # test with local PDF, skips HF/ArXiv fetch
```

Required env vars: `MODEL` (LiteLLM model string), the matching provider API key, `TG_BOT_TOKEN`, `TG_CHANNEL_ID`. See `.env.example` for all provider options.

## Code architecture

The pipeline flows linearly through these modules:

1. `core/fetch_papers.py` — scrapes HuggingFace Papers → fetches ArXiv metadata → downloads PDFs to `papers/` (parallel, 8 threads)
2. `core/parsers/pdf_parser.py` — extracts text from PDFs via PyPDF; `PDFParser("pypdf")` is the only supported backend
3. `core/summarizers/summarize.py` — calls LiteLLM `acompletion()` async; model is set via `MODEL` env var; prompts are in `core/templates/summarize_paper.py`
4. `core/share/telegram.py` — sends formatted Markdown messages to Telegram channel

`core/main.py` is the orchestrator. `summarize_batch()` processes 5 papers concurrently via `asyncio.gather`.

## Key design decisions

- **LiteLLM for provider-agnostic LLM calls**: `litellm.acompletion(model=MODEL, ...)` works with OpenAI, Anthropic, Azure, Bedrock, Vertex, Ollama, and more. Switching providers is just an env var change.
- **Model string format**: `provider/model-name` (e.g. `openai/gpt-4o-mini`, `anthropic/claude-3-5-haiku-20241022`, `azure/my-deployment`). LiteLLM reads the right API key env var automatically per provider.
- **Async for I/O-heavy stages**: summarization and Telegram sends use asyncio. PDF downloads use ThreadPoolExecutor because `requests` is synchronous.
- **Batch size = 5**: balances provider rate limits vs. throughput. Adjust in `summarize_batch(batch_size=...)`.
- **No retry logic on PDF download**: if ArXiv is slow, downloads fail silently. This is a known gap.

## Adding features

**Switch LLM provider**: set `MODEL` in your `.env` to any LiteLLM-supported model string and provide the matching API key. No code changes needed.

**New output channel** (e.g., Slack, Discord): add a module under `core/share/` following the same async pattern as `telegram.py`, then wire it into `core/main.py`.

**New paper source**: add a fetcher function in `core/fetch_papers.py` that returns `List[Paper]` with `filepath_local` populated.

## Dependencies

Managed via `uv`. To add a package:
```bash
uv add <package>
```

Dev tools go in the `dev` group:
```bash
uv add --dev <package>
```
