# Prompts to paste into your coding agent

Works with Claude Code, Cursor, Codex and other coding agents that can run shell commands. The agent runs the commands. You approve the browser sign in.

## Deploy an app that already exists (not public)

```text
Deploy the app in this folder with Stacksync Enterprise OS so my team can use it. It is internal, so it must NOT be public.

1. Read the official instructions at https://enterprise-os.stacksync.ai/skill.md and follow them.
2. Install the EOS CLI if it is missing, then run `eos auth login` and wait for me to approve the browser sign in. Do not ask for my password or token.
3. Run `eos workspace current` and confirm the workspace with me before creating anything.
4. Check the folder for secrets (.env files, keys, credentials) and tell me what you find. Make sure the server listens on 0.0.0.0 and on the PORT environment variable.
5. Run `eos deploy --dry-run` with a project name that has only lowercase letters, numbers and hyphens. Show me the result and wait for my yes.
6. Deploy, print the app URL and the deployment id, and tell me who can open the app.
7. Save the skill with `eos skill save` and add a short note to AGENTS.md. Never store secrets in it.
```

## No app yet: deploy the sample

```text
I have nothing to deploy yet. Use the Stacksync Enterprise OS instructions at https://enterprise-os.stacksync.ai/skill.md, install the EOS CLI if needed, have me sign in with `eos auth login`, then run `eos project quickstart todo-list deploy` and tell me the URL.
```

## Check who can open my app

```text
List my apps with `eos app list` in the current workspace. For the app named <APP>, tell me who can use it today (specific members, all workspace members or public) and explain how to restrict it. Do not change any access without asking me.
```

## Add a database

```text
My app needs a PostgreSQL database. Follow the EOS instructions: create a database with a unique name, pass its connection string to the app only as a project-scoped deployment variable read by the server, and never print it or put it in source. Show me the plan before you create anything.
```

## Add an AI feature with a spending limit

```text
My app needs an AI feature. Run `eos inference models --json` and propose a model. Create an inference key with a small weekly USD limit that I choose, keep it only in the server's deployment variables, and never show it. Ask me for the limit before you create the key.
```

## Debug a failed deploy

```text
The last deploy failed. Run `eos deployment versions <PROJECT>` and `eos deployment logs <DEPLOYMENT_ID>`, tell me the cause in plain words, fix it locally, run `eos deploy --dry-run`, and wait for my yes before deploying again.
```

## Tighten access

```text
The app <APP> should only be used by these people: <EMAILS>. Check my workspace role, explain the options (Operator can use the app without seeing its configuration), and make the change only after I confirm the exact scope.
```
