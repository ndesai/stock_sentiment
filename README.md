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

Sends an email using gmail smtp.

## prerequisites

- [uv](https://astral.sh)
- [x.ai](https://x.ai) api key exported to `XAI_API_KEY` env var

## running

```
uv sync --locked
uv run main.py
```

Use `--help` to see available options:

```
uv run main.py --help
Usage: main.py [OPTIONS]

Options:
  -d, --debug                  Enable debug mode
  -v, --verbose                Enable verbose mode
  -dp, --debug-prompt TEXT     Set a debug prompt
  -se, --sender-email TEXT     Set a sender email
  -sp, --sender-password TEXT  Set a sender password
  -ml, --mailing-list TEXT     Set a mailing list
  --help                       Show this message and exit.
```