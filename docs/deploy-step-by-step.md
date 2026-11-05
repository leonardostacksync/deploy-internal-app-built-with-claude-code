# Deploy an internal app, step by step

For an app that already exists in a folder on your computer. No GitHub repository is needed: deployment runs from the folder.

## 1. Install the EOS CLI (once per computer)

macOS or Linux:

```sh
curl -fsSL https://enterprise-os.stacksync.ai/downloads/install.sh | sh
eos --version
```

Windows (PowerShell):

```powershell
$installer = Join-Path $env:TEMP 'eos-install.ps1'; Invoke-WebRequest -UseBasicParsing https://enterprise-os.stacksync.ai/downloads/install.ps1 -OutFile $installer; powershell -NoProfile -ExecutionPolicy Bypass -File $installer
```

Open a new terminal afterwards. The installer needs no administrator access. Update later with `eos update`.

## 2. Sign in and choose the workspace

```sh
eos auth login
eos workspace list
eos workspace current
eos workspace switch WORKSPACE_ID    # only if you have more than one
```

Sign in before you deploy anything sensitive. See [public vs workspace-only](public-vs-workspace-access.md).

## 3. Check the folder

```sh
python scripts/preflight.py path/to/app --project my-app
```

This repo's preflight checks the port, secrets, project name, manifest and size before you spend a deploy. See [the checklist](preflight-checklist.md).

## 4. Dry run

```sh
eos deploy --dry-run --project=my-app
```

A dry run uploads nothing and creates nothing. Review the project, source path and variable names.

## 5. Deploy

```sh
eos deploy --project=my-app --variable=APP_TITLE='Ops dashboard'
```

Let it stream. When it succeeds, EOS prints the **deployment id** (`dep_N`) and the **app URL**. Use that URL. Never build one by hand.

## 6. Verify

Open the URL, check it responds, and confirm who can open it.

```sh
eos app list
eos deployment list my-app
eos deployment versions my-app
```

## 7. When it fails

```sh
eos deployment logs dep_123
```

Fix the cause locally, run the dry run again, then redeploy. See [troubleshooting](troubleshooting.md).

## 8. Later changes

- Redeploy with the same `--project`. The name and workspace of an app are fixed.
- Variables you do not repeat stay unchanged. Variables you pass replace the old values.
- Memory and scaling: `--memory 1Gi --max-instances 20` (memory 512Mi, 1Gi, 2Gi or 4Gi; 1 to 20 instances). A change needs a new deployment version.
- A custom domain (EOS 5.1.0 and later, claimed workspace): `eos app domains add APP portal.example.com`, then copy the DNS records it prints. Up to five per app.

## No app yet?

```sh
eos project quickstart todo-list
eos project quickstart todo-list deploy
```

The first downloads a sample to-do app. The second also deploys it after you sign in. The download needs `curl`, `openssl` and `unzip`, and local development uses Node.js 24.
