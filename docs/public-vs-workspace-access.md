# Public URL or workspace-only? The one thing to get right

"Where do I deploy an internal app so only my team can reach it?" has a short answer and one trap.

## The trap: deploying without signing in

You can run `eos deploy` as your very first command, without signing in. EOS creates a **guest workspace** for you. That is convenient for a demo, but:

- Apps in a guest workspace are **public**: anyone with the URL can open them.
- A guest workspace allows one app and one database.
- It **expires 14 days after creation** unless you claim it by signing in.

Do not deploy anything sensitive from a guest workspace.

## The fix: sign in first

```sh
eos auth login      # opens a browser, you approve, done
eos workspace list
eos workspace current
```

Now a new app belongs to your account workspace, and **opens to all members of that workspace by default**. It is not public.

If you already deployed as a guest, signing in claims the guest workspace. The resources keep their IDs and URLs and stop expiring.

## Who can open the app (runtime access)

An app's access preset controls who can **use** it. It is separate from who can **configure** it.

| Preset | Who can use the app |
|---|---|
| Specific members | Active users with an explicit direct or group grant |
| All workspace members | Admins and Members automatically (external operators need an explicit grant) |
| Public, authentication required | Any active EOS account with valid credentials |
| Public, no authentication required | Anyone, including anonymous visitors |

New account apps default to **All workspace members**. New guest apps default to **Public, no authentication required**. Existing apps keep their preset when you redeploy. An Owner changes the preset in the web app. There is no dedicated CLI command for it.

## Who can configure it (resource roles)

| Role | Can |
|---|---|
| Owner | Configure, manage sharing, delete |
| Editor | Change configuration, deploy changes, read permitted logs and variables |
| Viewer | See that it exists and read approved metadata |
| Operator | Use the app. Cannot see or configure it in EOS |

Give people **Operator** to use an app without seeing its configuration. Workspace membership alone does not grant configuration access, and a workspace Admin is not automatically an Owner.

## You do not build a login

EOS handles authentication. Your app does not need its own login system. For app roles and tokens, see `eos app roles`, `eos app users` and `eos app tokens` in `eos --help`.

## Quick decision

| You want | Do |
|---|---|
| A throwaway demo anyone can see | Deploy as a guest. It lasts 14 days |
| An internal tool for your team | Sign in first. Default is all workspace members |
| Only three people | Sign in, then set Specific members |
| A customer-facing page | Sign in, then choose a public preset on purpose |

Read the [official Enterprise OS docs](https://docs.stacksync.com/enterprise-os) for the current rules, and see [Stacksync Enterprise OS](https://www.stacksync.com/enterprise-os).
