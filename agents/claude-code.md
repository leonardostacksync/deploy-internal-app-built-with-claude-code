# Deploy an app built with Claude Code

## The 2 minute version

1. Open Claude Code in the app folder.
2. Paste the prompt from [the first prompt in `prompts/prompts.md`](../prompts/prompts.md).
3. Claude Code installs the CLI if needed and asks you to approve the browser sign in. **You** sign in. It never needs your password or token.
4. It runs a dry run, shows it to you, and deploys after you say yes.

## Make it remember

Save Stacksync's own instructions for this project so future sessions follow them:

```sh
eos skill save .claude/skills/deploy-with-eos/SKILL.md
```

The default location is `.agents/skills/deploy-with-eos/SKILL.md`. Use the path above if you want Claude Code to find it as a project skill. Refresh it with the same command when the CLI changes.

Then add a short note to `CLAUDE.md` or `AGENTS.md`. See [`examples/AGENTS-memory-note.md`](../examples/AGENTS-memory-note.md). Never store tokens, keys or credentials in it.

## Permissions

Claude Code asks before running shell commands. Approve `eos` commands you recognize. Do not approve anything that prints or pipes a secret.

## Tips

- Say **"sign in first, this is not public"** so it does not deploy as a guest.
- Ask it to run [`scripts/preflight.py`](../scripts/preflight.py) before the dry run.
- If a deploy fails, ask it to read `eos deployment logs dep_N`, fix the cause and run a dry run before retrying.

Stacksync's MCP server does not manage EOS apps. The CLI does. The [Stacksync MCP server](https://www.stacksync.com/mcp) is for building syncs, workflows and Genies from an assistant.
