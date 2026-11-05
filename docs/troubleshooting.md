# Troubleshooting a deploy

Start with the log:

```sh
eos deployment list my-app
eos deployment versions my-app      # which version failed
eos deployment logs dep_123
```

| What you see | Why | What to do |
|---|---|---|
| Authentication required | The CLI sign in expired | `eos auth login` |
| A resource is missing | Another workspace is selected, or you lack access | `eos workspace current`, then switch, or ask the owner to share it |
| An unknown command | The CLI is out of date | `eos update`, then `eos --help` |
| The container did not listen | The app ignores `PORT` or binds to localhost | Listen on `process.env.PORT` (or `$PORT`) on `0.0.0.0` |
| Build failed (lifecycle error) | A missing or conflicting manifest, lockfile, runtime or start command | Read the streamed build output and fix the manifest or start command |
| `413` or a size error | The compressed package is over 600 MiB | Remove generated assets and dependency folders |
| A hash collision message | Rare name clash | Choose a different project name. Do not work around it |
| Project name rejected | It has a period, or the URL label is over 63 characters | Use hyphens and a shorter name |
| No URL, or stalled output | An old CLI | `eos update` and retry |
| The app needs different variables | A variable is wrong | Redeploy with `--variable` for the keys that change. Others stay |
| The app works but strangers can open it | It was deployed as a guest, or the preset is public | Sign in, check the preset, see [public vs workspace-only](public-vs-workspace-access.md) |
| Guest workspace is gone | It expired after 14 days | Deploy again after signing in |

## Rules

- Fix the cause locally, run `eos deploy --dry-run`, then redeploy. Do not loop on real deploys.
- Never paste tokens or connection strings into a chat or a log.
- Do not choose another workspace to get around an access error.

More detail: [Enterprise OS docs](https://docs.stacksync.com/enterprise-os).
