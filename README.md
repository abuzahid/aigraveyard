# AI Graveyard

An archive of AI projects that shut down — plus **The Lifeboat**, a marketplace where
struggling "about to sink" projects can be listed for acquisition.

Full requirements: see `AI-Graveyard-BA-Document.md`.

## Stack

| Service | Tech | Role |
|---|---|---|
| `web` | Django 5 + DRF | REST API, SSR pages, admin CMS, all DB writes |
| `worker` | Celery | Listing expiry, moderation timers, digests |
| `realtime` | Node 22 + Socket.IO | Offer notifications, live counters (read-only DB) |
| `db` | PostgreSQL 16 | Single source of truth |
| `redis` | Redis 7 | Celery broker + cache + Django↔Node event bus |
| `nginx` | Nginx | Routes `/ws/` → Node, everything else → Django |

## Quick start

```bash
cp .env.example .env
docker compose up -d --build
```

On first boot the `web` container auto-runs `makemigrations`, `migrate`, loads the
seed fixture (13 TechCrunch graveyard entries), and creates the admin superuser.

- Site: http://localhost/ · tombstones at `/graves/<slug>/`
- API: `/api/graves/` · `/api/listings/` · `/api/stats/` (paginated, 20/page)
- Auth: `POST /api/auth/register/` (returns token) · `POST /api/auth/token/` · `GET /api/auth/me/`
- Django admin: http://localhost/django-admin/ (`admin` / `admin123`)
- Realtime health: http://localhost/ws/healthz — Socket.IO clients use path `/ws/socket.io` and `auth: { token: '<DRF_TOKEN>' }`

## Tests

```bash
docker compose exec web python manage.py test apps -v 1
```

CI runs the same suite on GitHub Actions (`.github/workflows/ci.yml`) with
Postgres + Redis services and a migration completeness check.

## Smoke test (offers + realtime event flow)

```bash
# 1. Register a seller and a buyer (token returned immediately)
curl -s -X POST http://localhost/api/auth/register/ -H 'Content-Type: application/json' \
  -d '{"username":"seller","password":"longpassword1","roles":["founder"]}'
curl -s -X POST http://localhost/api/auth/register/ -H 'Content-Type: application/json' \
  -d '{"username":"buyer","password":"longpassword1","roles":["buyer"]}'

# 2. Save a search (buyer gets an alert when a matching listing appears)
curl -s -X POST http://localhost/api/saved-searches/ -H "Authorization: Token <BUYER_TOKEN>" \
  -H 'Content-Type: application/json' \
  -d '{"filters":{"category":"productivity","min_mrr":1000},"alert_channel":"instant"}'

# 3. List a sinking project (seller) — triggers saved-search alerts via Celery
curl -X POST http://localhost/api/listings/ -H "Authorization: Token <SELLER_TOKEN>" \
  -H 'Content-Type: application/json' \
  -d '{"title":"AI Notes App","category":"productivity","pitch":"12K users but no runway",
       "asset_types":["codebase","user_base"],"pricing_mode":"offer",
       "metrics":{"mrr":1500,"users":12000},"runway_months":3,"stealth":false}'

# 4. Make an offer (buyer)
curl -X POST http://localhost/api/listings/1/offers/ -H "Authorization: Token <BUYER_TOKEN>" \
  -H 'Content-Type: application/json' -d '{"amount": "5000", "message": "I can save this"}'
# -> offer.new on Redis -> seller's socket room; alert.match -> matching buyers' rooms
```

## Architecture rules

1. **Django owns all writes.** The Node service connects to Postgres as `realtime_ro`
   (read-only, created by `db/init/00-create-readonly-role.sql`).
2. **Events flow over Redis pub/sub**: `offer.new`, `listing.new` (see `apps/core/events.py`
   and `realtime/src/server.js`).
3. Listing expiry (60 days) runs daily via Celery beat (`apps/lifeboat/tasks.py`).

## Status / roadmap

See `TRACKER.md` for the live build tracker.
