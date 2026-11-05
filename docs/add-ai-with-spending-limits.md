# Add AI to your internal app and cap what it spends

EOS provides AI inference through one API key, with a spending limit per key. Management uses your normal EOS sign in. Inference calls use a separate key that starts with `sk-ss-`.

```sh
eos inference models --json                  # pick an exact model id from the catalog
eos inference keys create 'Ops dashboard AI' --limit 10 --every 1 --unit weeks --json
```

The example is a $10 limit that resets every week. Pick your own numbers.

## What to know

- The full key is shown **once**. Capture it privately and put it in the app's deployment variables. Listing keys never shows it again.
- **Keep the key on the server.** Never in frontend code, a repo or a chat.
- `--limit` is USD (0 blocks requests). `--every` is 1 to 365 and `--unit` is days, weeks or months. Budgets do not roll over.
- Updating a key changes its name and limit without resetting spend. The schedule cannot change: create a new key for a different schedule.
- Choose a model from `eos inference models`. Do not hard-code an assumed model id.
- This endpoint is for text chat, function tools, JSON output options, reasoning and streaming.
- Inspect usage and logs:

```sh
eos inference usage
eos inference logs KEY_ID --json
```

- Revoking a key stops new requests and is irreversible.

## A safe pattern

1. One key per app, with a small weekly limit.
2. The server calls inference. The browser calls your server.
3. Log what the app sends and receives, and review the logs.
4. Raise the limit only after you have seen real usage.

An [AI agent that acts across your CRM and ERP](https://www.stacksync.com/ai-agents) is a different product from inference inside your own app. Use inference when your app needs a model. Use Genies when you want an agent that works in your connected systems.
