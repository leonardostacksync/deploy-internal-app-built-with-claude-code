"""Pre-deploy checks for an app folder you are about to deploy with the EOS CLI.

It catches the mistakes that fail a deploy or leak a secret: a server that does
not listen on the PORT the platform gives it, a .env file or private key in the
folder, a bad project name, a missing manifest, or a folder that is too large.

    python scripts/preflight.py path/to/app --project my-app --workspace-id 12345

It reads files only. It never uploads anything and never runs your app.
Standard library only. Python 3.9 or newer.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

# EOS excludes common dependency, VCS, cache, virtual-environment, coverage and log folders itself.
IGNORED_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", ".cache", "coverage", "logs", ".next", ".open-next", ".wrangler", "dist-cache"}
MAX_SOURCE_BYTES = 600 * 1024 * 1024  # the documented limit is for the COMPRESSED package
SECRET_FILE = re.compile(r"(^\.env(\..+)?$|\.pem$|\.key$|^id_(rsa|ed25519)(\.pub)?$|^credentials(\..+)?$|\.sql$|\.dump$|\.sqlite3?$|\.zip$|\.tar(\.gz)?$)", re.I)
SECRET_CONTENT = [
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "a private key"),
    (re.compile(r"\bsk-ss-[A-Za-z0-9]{10,}"), "an inference API key"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "an AWS access key id"),
    (re.compile(r"postgres(ql)?://[^:\s/]+:[^@\s]+@"), "a database connection string with a password"),
]
SOURCE_SUFFIXES = {".js", ".mjs", ".cjs", ".ts", ".py", ".go", ".rb"}
LISTEN = re.compile(r"\.listen\(|app\.run\(|serve_forever|ListenAndServe|HTTPServer\(|uvicorn\.run\(|\.start\(")
PORT_ENV = re.compile(r"process\.env\.PORT|os\.environ|os\.getenv|getenv\(|\$PORT|ENV\[.PORT.\]|Getenv\(", re.I)
LOOPBACK = re.compile(r"""['"](127\.0\.0\.1|localhost)['"]""")
TEST_FILE = re.compile(r"(^|/)(tests?/|test_[^/]*|[^/]*_test\.(py|go)|[^/]*\.(test|spec)\.[cm]?[jt]s|test\.[cm]?[jt]s)$")
NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MANIFESTS = ["package.json", "requirements.txt", "pyproject.toml", "go.mod", "Gemfile", "Procfile", "Dockerfile", "pom.xml"]


def walk(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORED_DIRS]
        for name in filenames:
            yield Path(dirpath) / name


def normalize(name: str) -> str:
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", name.lower())).strip("-")


def check_name(project: str, workspace_id: str | None) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if "." in project:
        errors.append(f"project name '{project}' contains a period. Use hyphens, for example '{project.replace('.', '-')}'")
    normalized = normalize(project)
    if not NAME.match(normalized):
        errors.append(f"project name '{project}' cannot be turned into lowercase letters, numbers and hyphens")
        return errors, warnings
    if normalized != project:
        warnings.append(f"EOS will normalize '{project}' to '{normalized}'")
    # The app URL is {project}-w{workspace_id}.stacksync.app and that DNS label must be at most 63 characters.
    ws = workspace_id or "0000000"
    label = f"{normalized}-w{ws}"
    if len(label) > 63:
        errors.append(f"'{label}' is {len(label)} characters. The combined label must be at most 63. Shorten the project name")
    elif not workspace_id and len(label) > 55:
        warnings.append("project name is long. Pass --workspace-id to check the 63 character limit exactly")
    return errors, warnings


def check_project(root: Path, project: str | None = None, workspace_id: str | None = None) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if not root.is_dir():
        return [f"{root} is not a folder"], warnings

    n_err, n_warn = check_name(project or root.resolve().name, workspace_id)
    errors += n_err
    warnings += n_warn

    files = list(walk(root))
    if not any((root / m).exists() for m in MANIFESTS):
        errors.append("no manifest found (package.json, requirements.txt, pyproject.toml, go.mod, Procfile, Dockerfile...). The build cannot tell what to run")
    pkg = root / "package.json"
    if pkg.exists():
        try:
            scripts = json.loads(pkg.read_text(encoding="utf-8")).get("scripts", {})
            if "start" not in scripts:
                warnings.append("package.json has no 'start' script. Add one so the platform knows how to start the app")
        except json.JSONDecodeError:
            errors.append("package.json is not valid JSON")

    total = 0
    for path in files:
        rel = path.relative_to(root)
        total += path.stat().st_size
        if SECRET_FILE.search(path.name):
            errors.append(f"{rel}: a file like this should not be deployed (secret, dump or archive). Remove it or keep it out of the folder")
        if path.suffix in SOURCE_SUFFIXES or path.name in {"Procfile"}:
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            for pattern, what in SECRET_CONTENT:
                if pattern.search(text):
                    errors.append(f"{rel}: contains {what}. Read secrets from deployment variables instead")
            if path.suffix in SOURCE_SUFFIXES and not TEST_FILE.search(rel.as_posix()) and LISTEN.search(text):
                if not PORT_ENV.search(text):
                    errors.append(f"{rel}: starts a server but never reads the PORT environment variable")
                if LOOPBACK.search(text):
                    errors.append(f"{rel}: binds to localhost. Listen on 0.0.0.0 so the platform can reach the app")
    if total > MAX_SOURCE_BYTES:
        warnings.append(f"folder is {total // (1024 * 1024)} MiB before compression. The compressed package must be at most 600 MiB")
    return errors, warnings


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder")
    parser.add_argument("--project", help="project name you will pass to eos deploy (default: the folder name)")
    parser.add_argument("--workspace-id", help="your numeric workspace id, to check the 63 character URL limit exactly")
    args = parser.parse_args()

    errors, warnings = check_project(Path(args.folder), args.project, args.workspace_id)
    for line in warnings:
        print(f"warning: {line}")
    for line in errors:
        print(f"error: {line}")
    if errors:
        print(f"\n{len(errors)} problem(s). Fix them, then run: eos deploy --dry-run")
        sys.exit(1)
    print("ok. Next: eos deploy --dry-run")


if __name__ == "__main__":
    main()
