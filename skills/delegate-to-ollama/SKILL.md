---
name: delegate-to-ollama
description: Route a prompt to a local Ollama model and return the response inline, as a manual failover when cloud usage limits hit or when a draft must stay fully local. Use when the user says "delegate to ollama", "/dto", "run this locally", "ask the local model", or hits a rate limit mid-task. Do NOT use for tasks needing workspace file reads, tool calls, or multi-step agentic work; the local model gets only the prompt text you send it.
aliases:
  - ollama
  - dto
---

# Delegate to Ollama

Send one prompt to a local Ollama instance, label whose words came back, and offer next steps. Done means: the response is displayed with its model name, and saved to `outputs/ollama/` if asked.

Two rules up front:

1. **Connection details come from config, never from this file.** Read `references/ollama-config.md` and `.env`; if neither has a base URL, ask once and offer to save it.
2. **Local-model output is a draft.** Label it with the model name, and never move it into `context/` without the user reviewing it.

## Read first

| Source | Path | What to extract |
|---|---|---|
| Ollama config | `references/ollama-config.md` (user-filled) | Base URL, default and fallback models, system prompt, routing table |
| Environment | `.env` (`OLLAMA_BASE_URL`, `OLLAMA_DEFAULT_MODEL`, `OLLAMA_FALLBACK_MODEL`) | Overrides for the same values |

## Usage

```
/dto <prompt>                      default model
/dto --model <name> <prompt>       specific model
/dto --save <prompt>               also write to outputs/ollama/
/dto --list                        show models on the instance
/dto --test                        connectivity check
```

## Workflow

### 1. Parse flags

`--model`, `--save`, `--list`, `--test`; everything else is the prompt.

### 2. Handle list/test

```bash
curl -s "$OLLAMA_BASE_URL/api/tags"
```

Print a clean table (name, size, family) and stop.

### 3. Send the prompt

Use `/api/chat` (better instruction following than `/api/generate`), with the configured system prompt:

```bash
curl -s "$OLLAMA_BASE_URL/api/chat" -H "Content-Type: application/json" -d '{
  "model": "<model>",
  "stream": false,
  "messages": [
    {"role": "system", "content": "<system prompt from config>"},
    {"role": "user", "content": "<prompt>"}
  ]
}'
```

Extract `.message.content`. On connection failure: report it plainly, suggest `/dto --test`, and offer the fallback model if the failure was a timeout.

### 4. Present

Label the response with the model (`**qwen3-coder:30b via Ollama:**` style). With `--save`, write per `templates/saved-output.md`.

### 5. Offer follow-up

Refine here with full context, save to `outputs/`, or retry on a different model from the routing table.

## Worked example (fictional)

A PM at Coppermine Systems, rate-limited mid-afternoon: `/dto Draft three subject lines for the fleet-migration announcement email`. The skill reads the config (default `qwen3-coder:30b` at `http://10.0.0.40:11434`), sends the prompt with the configured system prompt, and returns:

> **qwen3-coder:30b via Ollama:**
> 1. Fleet migration opens June 3: what changes for your devices
> 2. ...

Then: "Want me to refine these here once limits reset, or save as a draft?"

## Don't rationalize

| If you're thinking | Do this instead |
|---|---|
| "I'll just inline the host, config indirection is overhead" | Hosts and models change; hardcoded ones rot and leak infrastructure details into shared skills. |
| "The local output is good enough to file directly" | It skipped every workspace guardrail (style rules, context checks). Present it as a labeled draft. |
| "The task needs one file's contents, I'll paste them in" | Fine for one small file the user offered; beyond that the task needs tools, which is the boundary. Keep it here. |

## Exit checklist

Before finishing, verify:

- [ ] Connection details came from config or `.env`, not from memory or this file
- [ ] Response is labeled with the model that produced it
- [ ] `--save` output follows `templates/saved-output.md`, including the verbatim prompt
- [ ] A follow-up was offered (refine with context, save, or reroute)

## Handoff

- **Before this:** nothing required; this is a failover and offload path.
- **After this:** bring the draft back into a full-context session for refinement before it's used anywhere that matters.
