# Deploy an app built with Cursor

## The 2 minute version

1. Open the app folder in Cursor and use Agent mode with terminal access.
2. Paste the prompt from [the first prompt in `prompts/prompts.md`](../prompts/prompts.md).
3. Approve the terminal commands you recognize and **sign in yourself** in the browser when `eos auth login` prints the URL.
4. Review the dry run and say yes to deploy.

## Make it remember

```sh
eos skill save
```

This writes `.agents/skills/deploy-with-eos/SKILL.md`, the default. Saving the skill makes it available to future sessions. It does not guarantee that an agent loads it automatically, so add a pointer to it in `AGENTS.md` or a project rule. See [`examples/AGENTS-memory-note.md`](../examples/AGENTS-memory-note.md).

## Tips

- Tell Cursor to **sign in before deploying** so the app is not public.
- Ask it to run [`scripts/preflight.py`](../scripts/preflight.py) first.
- Keep secrets out of the folder. Cursor can see your `.env`, and EOS deploys the folder.
- If the CLI is missing a command, `eos update` then `eos --help`.
