# Preflight checklist

Run `python scripts/preflight.py <folder> --project <name>` for the automatic part.

## The app must

- [ ] **Listen on the `PORT` environment variable.** The platform sets it at run time. Do not hard-code a port
- [ ] **Listen on `0.0.0.0`**, not `localhost` or `127.0.0.1`
- [ ] Have a **manifest** (`package.json`, `requirements.txt`, `pyproject.toml`, `go.mod`, `Procfile`, `Dockerfile`) and a start command
- [ ] Read configuration from **environment variables**
- [ ] Have a **health check** route (not required, but it makes verification easy)

## The folder must not contain

- [ ] A local `.env` file
- [ ] Private keys, credential files or tokens
- [ ] Database dumps, customer data or archives
- [ ] Hard-coded database passwords or API keys in source

EOS excludes common dependency, version control, cache, virtual environment, coverage and log folders itself, and generated `.next/`, `.open-next/` and `.wrangler/` folders in recent versions. The compressed source must be **at most 600 MiB**.

## The project name must be

- [ ] Lowercase letters, numbers and hyphens only
- [ ] **No periods.** A folder called `my-app.v2` needs `--project my-app-v2`
- [ ] Short enough: the app URL is `https://{project}-w{workspace_id}.stacksync.app` and that label must be at most 63 characters
- [ ] Unique inside the workspace

## Before you press deploy

- [ ] You are **signed in** if the app is not meant to be public
- [ ] `eos workspace current` shows the workspace you intend
- [ ] `eos deploy --dry-run` looks right

## After

- [ ] The URL responds
- [ ] The access preset is what you intended
- [ ] You saved the deployment id
