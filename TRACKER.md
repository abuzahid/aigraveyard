# AI Graveyard — Build Tracker

Legend: ⬜ pending · 🔄 in progress · ✅ done · ❌ blocked

## Development

| # | Component | Status |
|---|---|---|
| 1 | Infra: docker-compose, nginx, db init, .env | ✅ done |
| 2 | Django config (settings, celery, urls) | ✅ done |
| 3 | App: accounts (User + roles, me endpoint) | ✅ done |
| 4 | App: graveyard (Grave, Submission, Reactions, API, admin, seed fixture) | ✅ done |
| 5 | App: lifeboat (Listing, Offer, Threads, SavedSearch, tasks, API) | ✅ done |
| 6 | App: analytics (stats endpoint) | ✅ done |
| 7 | Home page template (SSR) | ✅ done |
| 8 | Node realtime service (Socket.IO, redis-sub, counters) | ✅ done |

## Backlog Round 2 (2026-10-26)

| # | Item | Status |
|---|---|---|
| B1 | Public registration (`/api/auth/register/`) + token endpoint (`/api/auth/token/`) | ✅ done |
| B2 | Pagination on all list endpoints (PageNumberPagination, 20/page) | ✅ done |
| B3 | Tombstone detail SSR pages (`/graves/<slug>/`) + candle toggle | ✅ done |
| B4 | SavedSearch matching engine (Celery `dispatch_savedsearch_alerts` + `alert.match` push) | ✅ done |
| B5 | Weekly newsletter digest (Celery beat → email to `notify_digest` subscribers) | ✅ done |
| B6 | Unit tests — 33 tests across 5 apps | ✅ done |
| B7 | CI — GitHub Actions with Postgres/Redis services | ✅ done |

## Testing & Verification

| # | Check | Result |
|---|---|---|
| T1 | Python syntax check (compileall backend) | ✅ pass |
| T2 | docker-compose.yml validation | ✅ pass |
| T3 | Full stack boots — 6 containers, migrations, 31 seed records | ✅ pass |
| T4 | API smoke: graves (filters), stats, listings, offers, stealth | ✅ pass |
| T5 | Realtime: healthz, live counters (event-driven on listing.new) | ✅ pass |
| T6 | **33/33 Django tests pass** (accounts 7, graveyard 10, lifeboat 12, analytics 1, notify 1) | ✅ pass |
| T7 | Live smoke: register → token, pagination, `/graves/characterai/` SSR page | ✅ pass |
| T8 | `makemigrations --check` clean (migrations committed to repo) | ✅ pass |
| T9 | Celery beat schedule registered (daily expiry + weekly digest) | ✅ pass |

## Bugs found & fixed

### Round 1 (initial build)
1. Fixture path in compose `loaddata` command → `loaddata graves`
2. Realtime first-boot race (tables not migrated) → retry loop
3. Volume mount hid image `node_modules` → anonymous volume
4. Fixture needed explicit `created_at`/`updated_at`
5. Socket.IO path → `/ws/socket.io` to match nginx routing
6. Listing create serializer: category by slug, response echoes `id`

### Round 2 (backlog)
7. **`Listing.save()` 60-day expiry never applied** — compared `expires_at == timezone.now()` at save time (never true); now null-default + explicit set on create
8. `RegisterView`/`SubmissionCreateView` inherited `IsAuthenticatedOrReadOnly` → 401 on public POSTs; now `AllowAny`
9. `GraveViewSet` used pk lookup; API detail by slug now (`/api/graves/<slug>/`)
10. Submission payload crashed on `date` objects (not JSON-serializable) → stringified
11. Stats cache leaked between tests → cleared in test setUp

## Remaining backlog (v1 polish)

- ⬜ Comment API endpoints (model exists; only admin + SSR read today)
- ⬜ Stealth identity reveal for buyers who made an offer (US-3.5 full flow)
- ⬜ Message threads API (models exist, endpoints pending)
- ⬜ Production deployment (TLS, gunicorn already in Dockerfile, managed Postgres)
- ⬜ ESLint for realtime service in CI
