# Efficiency Calculator — API Reference

Internal doc for the `/api/calculate` endpoint.

---

## Endpoint

```
POST /api/calculate
```

---

## Request

**Headers:**
```
Content-Type: application/json
X-Api-Key: <key>          ← only required if API_KEY env var is set on the server
```

**Body:**
```json
{
  "value1":  46.8483,       ← latitude  (required, -90 … 90)
  "value2":  31.0821,       ← longitude (required, -180 … 180)
  "year":    2023,          ← optional, default 2023
  "turbine": "STANDARD_HAWT" ← optional: "STANDARD_HAWT" | "WITEROK", default "STANDARD_HAWT"
}
```

---

## Response

**Success `200`:**
```json
{ "result": 17431012.99 }
```
`result` is the estimated annual energy production in **kWh**.

**Errors:**

| Code | Meaning |
|------|---------|
| `400` | Invalid or missing input — `{ "error": "..." }` describes what's wrong |
| `401` | Missing or wrong `X-Api-Key` header |
| `429` | Rate limit hit (60 req/min per IP) — check `Retry-After` header |
| `500` | Calculation failed — `{ "error": "..." }` has details |

---

## Usage examples

**JS (fetch):**
```js
const res = await fetch('https://your-api-domain.com/api/calculate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-Api-Key': 'your-key',   // omit if no key is configured
  },
  body: JSON.stringify({ value1: 46.8483, value2: 31.0821 }),
});
const { result } = await res.json();
```

**PHP (backend → API):**
```php
$response = wp_remote_post('https://your-api-domain.com/api/calculate', [
  'headers' => ['Content-Type' => 'application/json', 'X-Api-Key' => 'your-key'],
  'body'    => json_encode(['value1' => 46.8483, 'value2' => 31.0821]),
]);
$data = json_decode(wp_remote_retrieve_body($response), true);
// $data['result'] → kWh value
```

**curl (quick test):**
```bash
curl -X POST https://your-api-domain.com/api/calculate \
  -H "Content-Type: application/json" \
  -d '{"value1": 46.8483, "value2": 31.0821}'
```

---

## Environment variables

Set these on the server before running:

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENWEATHER_API_KEY` | Yes | OpenWeather One Call 3.0 key |
| `FRONTEND_ORIGIN` | Yes | Full origin of the WordPress site, e.g. `https://example.com` |
| `API_KEY` | No | Shared secret for `X-Api-Key` header protection. Leave unset to disable. |
| `PYTHON_BIN` | No | Path to Python 3 interpreter. Defaults to `python3`. Point to a venv if needed. |

---

## Performance note

First request for a new lat/lon triggers ~365 OpenWeather API calls and can take 30–60 s.
Subsequent requests use the local cache and respond in **< 500 ms**.
Pre-warm the cache for known locations if cold-start latency is a concern.

---

## ⚠ Server setup — *caution: not sure if this is needed, providing just in case*

If the API lives on the **same server as WordPress** under a subdirectory (e.g. `/api/`), you may need to add this to the **root** `.htaccess` so WordPress doesn't intercept the route before it reaches the API:

```apache
# Add above the WordPress "BEGIN WordPress" block
RewriteRule ^api/(.*)$ /api/index.php [QSA,L]
```

The `api/.htaccess` handles routing within the `api/` directory itself, so this is only needed if WordPress's own rewrite rules are catching the request first.
