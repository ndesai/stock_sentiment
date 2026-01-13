# stock sentiment

stock sentiment analysis using [X.ai](https://x.ai) Grok

Each request is ~160,000 tokens, e.g.

```
completion_tokens: 2707
prompt_tokens: 45719
total_tokens: 51443
prompt_text_tokens: 45719
reasoning_tokens: 3017
cached_prompt_text_tokens: 14412
```

## prerequisites

- [uv](https://astral.sh)
- [x.ai](https://x.ai) api key exported to `XAI_API_KEY` env var

## running

```
uv sync --locked
uv run main.py
```
