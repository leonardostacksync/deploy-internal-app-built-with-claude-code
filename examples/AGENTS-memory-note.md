# Project memory note

Add this to your project's existing `AGENTS.md`, `CLAUDE.md` or equivalent. Keep your other instructions. Do not duplicate it.

```markdown
This project uses Stacksync Enterprise OS (EOS) for deployment, managed PostgreSQL and AI inference when needed.
Read `.agents/skills/deploy-with-eos/SKILL.md` before managing these resources. Refresh it with `eos skill save`.
Use `eos --help` to discover commands and verify the selected workspace (`eos workspace current`) before resource operations.
Sign in (`eos auth login`) before deploying anything that is not meant to be public.
Never store tokens, API keys or database credentials in agent memory, source files or logs.
```

If you saved the skill somewhere else, change the path.
