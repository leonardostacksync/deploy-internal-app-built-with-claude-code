# Give your internal app a Postgres database

An app can have its own managed PostgreSQL database with dedicated credentials. Stacksync creates an isolated database and a dedicated login role with a random password for each one.

```sh
eos database list
eos database create 'ops-dashboard-20261105-a1b2c3'
eos database credentials DATABASE_ID
```

`create` returns the connection string. Treat it, and the database id, as a secret.

## Rules that save you later

1. **Use a unique database name** per project and run. Not `app`, `development` or the bare repository name. Several projects can share one machine and names are compared case-insensitively.
2. **Use a project-scoped variable name** for the connection string, for example `DATABASE_CONNECTION_STRING_FOR_APP_OPS_DASHBOARD`, so one app cannot overwrite another's.
3. **Pass it as a deployment variable** and read it on the server. Never put it in source, frontend code or a chat.
4. **Do not reuse a database found by fuzzy name matching.** Reuse one only when you identify it.
5. **Deleting is permanent.** `eos database delete ID NAME` removes the data and the role. Ask first.

```sh
eos deploy --project=ops-dashboard \
  --variable=DATABASE_CONNECTION_STRING_FOR_APP_OPS_DASHBOARD="$CONNECTION_STRING"
```

(Read `$CONNECTION_STRING` from a place that does not print it. Do not echo it.)

## Want the data to come from your CRM or ERP?

An app that needs live Salesforce, NetSuite or HubSpot data does not have to call those APIs itself. [Two-way sync](https://www.stacksync.com/two-way-sync) can keep a current copy in a database your app reads, and writes flow back within the mappings you configure. The database of an app is connected to Stacksync like any other database.
