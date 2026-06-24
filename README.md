# Synopso

Synopso fetches the day's top AI research papers from [HuggingFace Papers](https://huggingface.co/papers), summarizes them using any LLM via [LiteLLM](https://docs.litellm.ai), and sends the summaries to a Telegram channel.

## How it works

1. Scrapes the HuggingFace papers page to get the day's curated ArXiv papers
2. Downloads PDFs from ArXiv in parallel (8 workers)
3. Extracts text from each PDF
4. Summarizes each paper with your chosen LLM (batched, async)
5. Sends formatted summaries to a Telegram channel

## Setup

**Requirements:** Python 3.12+, [uv](https://github.com/astral-sh/uv)

```bash
git clone https://github.com/yourusername/synopso
cd synopso
uv sync
cp .env.example .env  # then fill in your keys
```

### Environment variables

Set `MODEL` to any [LiteLLM-supported model string](https://docs.litellm.ai/docs/providers) and provide the matching API key for your provider:

| Provider | `MODEL` | Key env var |
|----------|---------|-------------|
| OpenAI | `openai/gpt-4o-mini` | `OPENAI_API_KEY` |
| Anthropic | `anthropic/claude-3-5-haiku-20241022` | `ANTHROPIC_API_KEY` |
| Azure OpenAI | `azure/your-deployment` | `AZURE_API_KEY`, `AZURE_API_BASE`, `AZURE_API_VERSION` |
| Google Vertex | `vertex_ai/gemini-1.5-flash` | `VERTEXAI_PROJECT`, `VERTEXAI_LOCATION` |
| AWS Bedrock | `bedrock/anthropic.claude-...` | `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION_NAME` |
| Ollama (local) | `ollama/llama3` | *(none)* |

Plus Telegram credentials:
```
TG_BOT_TOKEN=
TG_CHANNEL_ID=
```

- **Telegram**: Create a bot via [@BotFather](https://t.me/botfather), add it to your channel, and get the channel ID.

## Usage

```bash
# Run the full pipeline
uv run python -m core.main

# Test with a local PDF (no network fetch, sends to Telegram)
uv run python -m core.main --test
```

Downloaded PDFs are saved to `papers/` in the project root (git-ignored).

## Project structure

```
synopso/
├── core/
│   ├── main.py              # Entry point and pipeline orchestration
│   ├── models.py            # Paper dataclass
│   ├── fetch_papers.py      # HuggingFace scraping + ArXiv PDF download
│   ├── parsers/
│   │   └── pdf_parser.py    # PDF text extraction (PyPDF)
│   ├── summarizers/
│   │   └── summarize.py     # LiteLLM summarization
│   ├── templates/
│   │   └── summarize_paper.py  # LLM prompt templates
│   └── share/
│       └── telegram.py      # Telegram message delivery
└── test/
    └── test.pdf             # Sample PDF for --test mode
```

## Tech stack

| Component | Library |
|-----------|---------|
| Web scraping | beautifulsoup4 + lxml |
| HTTP | requests |
| PDF parsing | pypdf |
| LLM | litellm (any provider) |
| Telegram | python-telegram-bot |
| Concurrency | asyncio + ThreadPoolExecutor |
| Package manager | uv |

## Automating with cron

To run daily (e.g. every morning at 8am):

```
0 8 * * * cd /path/to/synopso && uv run python -m core.main >> logs/synopso.log 2>&1
```

## License

MIT
