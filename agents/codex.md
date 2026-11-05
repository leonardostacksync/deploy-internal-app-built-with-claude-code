# Deploy an app built with Codex

## The 2 minute version

1. Run Codex in the app folder.
2. Paste the prompt from [the first prompt in `prompts/prompts.md`](../prompts/prompts.md).
3. Approve the browser sign in yourself. Codex does not need your token.
4. Review the dry run, then approve the deploy.

## Make it remember

```sh
eos skill save .codex/skills/deploy-with-eos/SKILL.md
```

Add the short note from [`examples/AGENTS-memory-note.md`](../examples/AGENTS-memory-note.md) to your `AGENTS.md`. Refresh the saved skill with the same command when the CLI changes.

## Tips

- Say clearly that the app is internal and you must be **signed in** before the deploy.
- Run [`scripts/preflight.py`](../scripts/preflight.py) before the dry run.
- After a failure, read `eos deployment logs dep_N` before another real deploy.
