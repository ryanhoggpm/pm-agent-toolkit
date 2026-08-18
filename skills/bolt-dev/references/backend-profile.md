# Backend profile (fill this in once per project)

`/bolt-dev` reads this file to generate your Bolt Project Knowledge, Vite proxy config, and session prompts without re-asking every time. One profile per frontend project; keep it next to the project's other context.

| Field | Value | Notes |
|---|---|---|
| Project name | | |
| GitHub repo | | Bolt connects here; work happens on a `bolt-dev` branch, never `main` |
| API base URL | | The host the Vite proxy targets |
| Auth pattern | | Header names and token source; where tokens are stored client-side |
| API versions in play | | e.g. "v1 and v2 co-exist; check per endpoint" |
| Real-time transport | | MQTT / WebSocket / SSE / none, with connection URL |
| Design direction | | Palette, density, desktop vs mobile priority; link brand tokens if you have them |
| Domain glossary | | 5-8 terms the UI must use consistently |
| Known API quirks | | Anything a code generator would get wrong; feed findings from /api-review here |

## Example (fictional): Coppermine Systems device cloud

| Field | Value |
|---|---|
| Project name | Coppermine Console |
| GitHub repo | `github.com/coppermine-io/console-frontend`, branch `bolt-dev` |
| API base URL | `https://api.coppermine.example` |
| Auth pattern | `X-Session-Token` + `X-CSRF-Token` headers on every request; tokens live in React context, never localStorage |
| API versions in play | v2 is primary; `/jobs` endpoints are still v1 |
| Real-time transport | MQTT over `wss://mqtt.coppermine.example:443/mqtt` for device status |
| Design direction | Dark slate palette, data-dense tables, desktop-primary |
| Domain glossary | Device, Port, Site, Fleet Group, Telemetry, Job |
| Known API quirks | `POST /jobs` is one-shot only (no schedules); device list paginates at 100 with no page-size param |
