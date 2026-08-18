# Workspace setup

The skills in this toolkit read from and write to a small set of standard folders. Set them up once and every skill's read-first table works without editing.

```
your-workspace/
├── context/            # your knowledge base: strategy docs, research, meeting notes, stakeholder profiles
│   └── reference/      # product docs, specs, external material
├── outputs/            # everything skills generate for you
└── .claude/
    └── skills/         # if installing by manual copy
```

Two conventions the skills assume:

1. **`context/` is yours, `outputs/` is the toolkit's.** Skills never modify `context/`; they read it. Generated work lands in `outputs/<type>/`. Move a finished document into `context/` yourself when it becomes part of your record.
2. **Paths are defaults, not requirements.** Every skill's read-first table names paths under `context/` and `outputs/`. If your workspace differs, note the mapping once in your project's `CLAUDE.md` ("my context lives in kb/") and Claude adapts.

## CLAUDE.md starter

A minimal project CLAUDE.md that makes the toolkit's skills context-aware:

```markdown
# Workspace

- Knowledge base: `context/` (strategy, research, meetings, stakeholders)
- Generated work: `outputs/`, organized by type
- My role: [your role, product area, company stage]
- Writing style: [3-5 rules; see rules/writing-style.md in pm-agent-toolkit for a starting set]
```

More detail in [the-system-layer.md](the-system-layer.md) for hooks and rules.
