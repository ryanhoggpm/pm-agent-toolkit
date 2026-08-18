# Ollama config (fill this in once)

`/delegate-to-ollama` reads connection details from here (or from matching environment variables in `.env`, which win when both exist). Never hardcode hosts or model names in the skill itself; instances change.

| Setting | Env var | Value | Notes |
|---|---|---|---|
| Base URL | `OLLAMA_BASE_URL` | `http://localhost:11434` | Your Ollama host; LAN IPs are fine here, never in skill files |
| Default model | `OLLAMA_DEFAULT_MODEL` | | Your best general-purpose local model |
| Fallback model | `OLLAMA_FALLBACK_MODEL` | | Smaller/faster model when the default is busy or too slow |
| System prompt | | | One or two sentences: who the assistant is drafting for, and your style rules |

## Model routing table (edit for what you actually run)

| Task type | Model | Why |
|---|---|---|
| Code generation, technical analysis | (default) | |
| Long-form writing, summarization | | |
| Multi-step reasoning | | |
| Fast drafts | (fallback) | |

## Example (fictional)

A PM at Coppermine Systems runs:

| Setting | Value |
|---|---|
| Base URL | `http://10.0.0.40:11434` |
| Default model | `qwen3-coder:30b` |
| Fallback model | `qwen2.5-coder:7b` |
| System prompt | "You draft for a product manager at a B2B device-management company. Concise, specific, professional. No buzzwords." |
