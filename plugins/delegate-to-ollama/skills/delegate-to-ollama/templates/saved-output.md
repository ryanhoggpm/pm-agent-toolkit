# Saved output format (--save flag)

Write to `outputs/ollama/YYYY-MM-DD-<first-5-words-of-prompt-slug>.md`:

```markdown
---
model: [model name]
date: YYYY-MM-DD
prompt: |
  [the original prompt, verbatim]
---

[the model's response, unedited]
```

The file is a draft from a local model, not reviewed work. It never moves into `context/` without a human read-through.
