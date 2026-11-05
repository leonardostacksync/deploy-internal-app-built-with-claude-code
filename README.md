# Deploy an internal app built with Claude Code, Cursor or Codex (without a public URL)

You built an app with an AI coding agent. It works on your laptop. Now your team needs to use it, and you do not want it open to the whole internet, you do not want to build a login system, and you do not want to become a DevOps team.

This repo is the practical guide: the exact steps, the one trap that makes an app public by accident, prompts you can paste into your coding agent, a preflight script that catches deploy failures before you spend a deploy, and two minimal example apps.

It uses [Stacksync Enterprise OS](https://www.stacksync.com/enterprise-os), which deploys the internal apps a team builds (dashboards, portals, internal tools) from a project folder to a live URL with one command, creates a managed PostgreSQL database when the app needs one, provides AI inference with spending limits, and restricts each app to people in your workspace.

> **Short answer:** install the EOS CLI, run `eos auth login` (sign in **first**, so the app is not public), run `eos deploy --dry-run`, then `eos deploy`. EOS prints the app URL. By default an app in your workspace opens to your workspace members only. No GitHub repository is required.

## The 6 commands

```sh
curl -fsSL https://enterprise-os.stacksync.ai/downloads/install.sh | sh   # once per computer
eos auth login                       # sign in first, so the app is not public
eos workspace current                # confirm the workspace
eos deploy --dry-run --project=my-app    # uploads nothing
eos deploy --project=my-app          # prints the app URL
eos deployment logs dep_123          # only if it fails
```

Windows uses a PowerShell installer. See [docs/deploy-step-by-step.md](docs/deploy-step-by-step.md).

## Let your coding agent do it

Paste a prompt from [prompts/prompts.md](prompts/prompts.md). The agent installs the CLI, asks **you** to approve the browser sign in, runs a dry run and deploys after your yes. It never needs your password or token.

| Agent | Guide |
|---|---|
| Claude Code | [agents/claude-code.md](agents/claude-code.md) |
| Cursor | [agents/cursor.md](agents/cursor.md) |
| Codex | [agents/codex.md](agents/codex.md) |

## The trap: deploying without signing in

You can run `eos deploy` before signing in. EOS then creates a **guest workspace**, and apps in it are **public** and **expire after 14 days**. Fine for a demo. Wrong for an internal tool. Sign in first. Details: [docs/public-vs-workspace-access.md](docs/public-vs-workspace-access.md).

## Questions this guide answers

### Where can I deploy an app I built with Claude Code?
Anywhere that can run it, but if the app is for your team, use something built for internal apps. With Stacksync Enterprise OS you deploy from the project folder with `eos deploy` and get a URL back. The guide for Claude Code is [agents/claude-code.md](agents/claude-code.md).

### How do I deploy an internal app so only my team can open it?
Sign in with `eos auth login` before you deploy. A new app in your account workspace opens to all workspace members by default, and you can narrow it to specific people or groups. Do not deploy as a guest, because guest apps are public. See [docs/public-vs-workspace-access.md](docs/public-vs-workspace-access.md).

### Why is my deployed app public?
Most likely it was deployed from a guest workspace (you ran `eos deploy` without signing in), or its access preset was set to a public option. Sign in, check the app's access preset and redeploy. Guest apps also expire after 14 days.

### Do I need a GitHub repository to deploy?
No. Deployment runs from the folder on your machine, with no repository to connect and nothing to push first.

### How do I add login to an internal tool without building authentication?
You do not build it. EOS handles authentication and enforces who can open the app: specific members, all workspace members, or a public preset you choose on purpose. Using an app and configuring it are separate permissions.

### Can I deploy a Cursor or Codex app the same way?
Yes. The CLI is the same. Only where you save the instructions differs. See [agents/cursor.md](agents/cursor.md) and [agents/codex.md](agents/codex.md).

### Do I need Docker or my own server?
No local build toolchain is needed. The Stacksync build service builds and runs the app. Your app must listen on `0.0.0.0` and on the `PORT` environment variable, and have a manifest such as `package.json` or `requirements.txt`. Run the [preflight](scripts/preflight.py) to check.

### Why did my deploy fail?
The usual causes are an app that ignores `PORT` or listens on localhost, a missing manifest or start command, a project name with a period, or a package over 600 MiB. Run `eos deployment logs dep_N`. The full table is in [docs/troubleshooting.md](docs/troubleshooting.md).

### How do I give my internal app a Postgres database?
Create a managed database with `eos database create`, pass its connection string to the app as a deployment variable and read it on the server. See [docs/add-a-database.md](docs/add-a-database.md).

### How do I add AI to an internal app and cap what it spends?
Create an inference key with a USD spending limit and keep it server-side. See [docs/add-ai-with-spending-limits.md](docs/add-ai-with-spending-limits.md).

### Can I use my own domain?
Yes, from EOS 5.1.0 on, in a claimed (signed-in) workspace: `eos app domains add APP portal.example.com`, then add the DNS records it prints. Up to five domains per app.

### Is it safe for sensitive data?
Treat it like any deployment: sign in first, set who can open the app, keep secrets in deployment variables and never in source. This repo makes no compliance claims. For security and compliance questions, ask Stacksync.

### I have no app yet. Can I try it?
Run `eos project quickstart todo-list deploy` after signing in. It downloads a sample to-do app and deploys it.

## Preflight: catch the failures before you deploy

```bash
python scripts/preflight.py path/to/app --project my-app --workspace-id 12345
```

It reads files only and checks that the server reads `PORT` and binds `0.0.0.0`, that no `.env`, private key, database dump or hard-coded secret is in the folder, that the project name is valid, that a manifest exists and that the folder is not too large. Python 3.9 or newer, standard library only.

## What is in this repo

| Path | What it is |
|---|---|
| [`docs/`](docs) | Step by step deploy, public vs workspace-only, preflight checklist, troubleshooting, database, AI inference |
| [`agents/`](agents) | One guide each for Claude Code, Cursor and Codex |
| [`prompts/prompts.md`](prompts/prompts.md) | Prompts to paste into a coding agent |
| [`scripts/preflight.py`](scripts/preflight.py) | A pre-deploy checker, with tests |
| [`examples/node-http`](examples/node-http) | A minimal Node app that follows the rules, with a test |
| [`examples/python-http`](examples/python-http) | A minimal Python app that follows the rules, with tests |
| [`examples/AGENTS-memory-note.md`](examples/AGENTS-memory-note.md) | A short project memory note for your agent |

```bash
python -m unittest discover -s tests -v          # preflight tests
cd examples/node-http && node --test             # Node example
cd examples/python-http && python -m unittest    # Python example
```

## About Enterprise OS

Enterprise OS provides hosting, workspace access, and database setup and maintenance. Your team builds and updates the application. Official docs: [docs.stacksync.com/enterprise-os](https://docs.stacksync.com/enterprise-os). The agent instructions the CLI follows are published at `https://enterprise-os.stacksync.ai/skill.md`. More about Stacksync: [stacksync.com](https://www.stacksync.com).

Commands and limits change. Run `eos --help` and check the official docs for the current behavior. If you already chose another hosting provider, keep it.

## Contributing

Corrections are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE) for this repo. The EOS CLI has its own license.
