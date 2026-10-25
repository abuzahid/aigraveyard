# AI Graveyard — Business Analysis Document

**Project Name:** AI Graveyard (working title)
**Document Type:** Business Analysis / Product Requirements Document (BRD-lite)
**Version:** 1.0 (Draft)
**Date:** 2026-10-26
**Prepared by:** Senior Business Analyst
**Status:** For Review

---

## 1. Executive Summary

AI Graveyard is a web platform that archives, documents, and analyzes AI projects, products, and startups that have shut down or are at risk of failure. According to S&P Global Market Intelligence, ~42% of AI initiatives are ultimately abandoned, and high-profile failures (Character.ai bankruptcy, Sora shutdown, Humane AI Pin, Huxe, Yupp, Relay, Notion Mail) continue to accumulate monthly.

The platform has two core pillars:

1. **The Graveyard (Archive)** — a curated, searchable archive of AI projects that completely shut down, pivoted, or dramatically missed expectations.
2. **The Lifeboat (Marketplace)** — a listing marketplace for AI projects that are "about to sink" — struggling but still alive — where founders can list their project, user base, code, IP, or entire company for acquisition by buyers who can rescue or repurpose them.

The objective is to become the industry's reference point for AI failure data ("what died and why") while monetizing the rescue/liquidity side of the market.

---

## 2. Problem Statement

| Stakeholder | Pain Point |
|---|---|
| Founders of failing AI startups | No graceful exit: shutdown announcements waste assets (code, users, brand, domain, trained models). No dedicated marketplace for small/mid AI asset sales. |
| Buyers / acquirers / indie hackers | No centralized place to discover undervalued AI projects with existing users or tech available for acquisition. |
| Industry analysts, journalists, VCs | Failure data is scattered across news articles, X/Twitter threads, and forum posts. No structured dataset of "what failed, when, why, and how much was burned." |
| New AI founders | Repeat the same mistakes because post-mortem knowledge is not aggregated or structured. |

---

## 3. Vision & Objectives

**Vision Statement:** "No AI project should die in silence — every failure should teach the industry, and every sinking project deserves a lifeboat."

**Business Objectives (Year 1):**

| # | Objective | KPI |
|---|---|---|
| O1 | Build the most complete archive of dead AI projects | 1,000+ documented entries |
| O2 | Establish the Lifeboat marketplace as a known exit route for struggling AI founders | 100+ active listings, 10+ completed acquisitions |
| O3 | Build audience and authority (SEO/PR flywheel) | 250K monthly visits |
| O4 | Achieve initial revenue | $5K MRR by month 12 |

---

## 4. Scope

### 4.1 In Scope (v1)
- Public web platform (desktop + mobile web)
- Two main sections: Graveyard (archive) and Lifeboat (marketplace)
- User accounts (founders, buyers, browsers)
- Submission and moderation workflows
- Newsletter / notification system
- Admin CMS for curation

### 4.2 Out of Scope (v1)
- Native mobile apps
- Escrow/ payment settlement for acquisitions (handled manually or via partner in v1; direct payments deferred to v2)
- Community forum (defer; comments suffice initially)

---

## 5. Target Users & Personas

**P1 — The Historian (Browser/Reader):** Developers, AI enthusiasts, journalists, analysts. Wants to browse/search dead projects, read post-mortems, see failure statistics.

**P2 — The Survivor (Seller/Founder):** Founder of a struggling AI product with real users or tech but no runway. Wants a dignified, fast exit — sell the product, code, domain, user base, or whole company.

**P3 — The Salvager (Buyer/Acquirer):** Indie hacker, SME, or corp-dev team looking to buy undervalued AI assets — users, tech, talent, or brand — cheaper than building from scratch.

**P4 — The Curator (Admin/Moderator):** Internal team or trusted editors who verify entries, approve listings, and maintain data quality.

---

## 6. Feature List

### 6.1 Core — The Graveyard (Shut-Down Archive) — MVP

| ID | Feature | Description | Priority |
|---|---|---|---|
| G-01 | Project Tombstone Page | Structured page per dead project: name, logo, category, lifecycle dates (born/died), funding raised, cause-of-death category (funding, competition, no PMF, legal/regulatory, technical, pivot, absorbed-by-parent), description, and a "what we learned" note. | Must |
| G-02 | Search & Filter | Search by name; filter by category (chatbot, hardware, video, audio, dev tools…), cause of death, funding size, year of shutdown, geography. | Must |
| G-03 | Timeline / Feed | Reverse-chronological feed of newly added deaths; "RIP This Month" section. | Must |
| G-04 | Submission Form | Community submissions of dead projects with source links (news article, official announcement). | Must |
| G-05 | Moderation & Verification | Admin workflow to verify submissions against sources before publishing (prevents fake deaths). | Must |
| G-06 | Statistics Dashboard | Aggregated charts: deaths per quarter, top causes of death, most burned capital, biggest graves (by funding raised). Highly shareable / SEO magnet. | Should |
| G-07 | Post-Mortem Articles | Editorial long-form "autopsy" write-ups (own or user-contributed) per major failure. | Should |
| G-08 | "Missed Expectations" Status | Not every entry is fully dead — support statuses: Dead / Pivoted / Absorbed / Delayed / Rollback (e.g., OpenAI super-app rollback, Apple Siri delays, Microsoft Recall). | Should |
| G-09 | Memorial Reactions | Light engagement: candles🕯 / "visited grave" reactions, comments on tombstones. | Could |
| G-10 | API & Data Export | Public read API of graveyard data (rate-limited); premium full-dataset download. | Could |

### 6.2 Core — The Lifeboat (Rescue Marketplace) — MVP

| ID | Feature | Description | Priority |
|---|---|---|---|
| L-01 | Listing Creation (Seller) | Founders list a sinking project: description, distress reason (optional), metrics (MRR, users, traffic, churn), tech stack, what's for sale (whole product / code / domain+brand / user base / team hire / customer list), and asking type (fixed price / make-offer / giveaway for continuity). | Must |
| L-02 | "Sinking Signal" Health Indicators | Seller-reported + optionally verified indicators: runway left, declining traffic, funding stalled. Displayed as a "water level" urgency indicator. | Should |
| L-03 | Listing Browsing & Filter (Buyer) | Browse/filter by category, price range, asset type, metrics (min MRR, min users), tech stack, urgency. | Must |
| L-04 | Private Contact / Offer Flow | Buyer-to-seller private messaging and non-binding offer submission. Platform facilitates introductions in v1; transactions settle outside the platform. | Must |
| L-05 | Watchlist & Alerts | Buyers save searches / follow categories and get notified when matching projects list themselves. | Should |
| L-06 | Verified Listings | Optional paid tier: platform verifies claimed metrics (screenshots of analytics, Stripe, etc.) with a "Verified" badge. | Should |
| L-07 | Success Stories | Published "rescued" case studies — projects that got acquired and survived (powerful marketing for both sides). | Should |
| L-08 | Anonymous Listing | Founders can list discreetly ("Stealth AI SaaS, $8K MRR, codebase for sale") to avoid public distress signals. | Could |
| L-09 | Escrow & Deal Rooms | V2: integrated offer–accept–escrow–asset-transfer flow with platform take-rate. | Future |

### 6.3 Platform-Wide

| ID | Feature | Description | Priority |
|---|---|---|---|
| P-01 | User Accounts & Profiles | Sign up (email/SSO), roles: reader, founder/seller, buyer. Public profiles showing listings or submissions. | Must |
| P-02 | Newsletter | Weekly "Who Died This Week" + "Sinking Ships to Save" digest. Primary audience-retention and monetization channel. | Must |
| P-03 | SEO-Optimized Structure | Structured tombstone pages (schema.org markup), category landing pages, comparison pages. Failures are high-search-volume, low-competition SEO. | Must |
| P-04 | Admin CMS | Manage entries, listings, users, verifications, sponsored placements. | Must |
| P-05 | Notifications | Email/in-app notifications for watchlists, offers, messages, followed categories. | Should |
| P-06 | Embeddable Widgets | "RIP counter" / graveyard stats widget blogs can embed (backlink growth loop). | Could |
| P-07 | Multi-language Support | Localized versions for non-English AI ecosystems (EU, India, SEA). | Future |

---

## 7. Revenue Model

### 7.1 Streams

| # | Stream | Mechanism | Type | Phase |
|---|---|---|---|---|
| R1 | **Marketplace Success Fee** | Commission on completed acquisitions facilitated through the Lifeboat (5–8% typical for micro-acquisitions). | Transaction | V1 (manual) → V2 (escrow) |
| R2 | **Featured / Boosted Listings** | Sellers pay to boost listing visibility or pin to top of Lifeboat (e.g., $49–$199 for 14 days). | Listing fee | V1 |
| R3 | **Verified Listing Fee** | Flat fee ($99–$249) for metric verification badge — increases buyer trust and seller's sale odds. | Service fee | V1 |
| R4 | **Newsletter Sponsorships** | Weekly "Who Died This Week" newsletter ad slots — natural fit for acquirers, M&A advisors, dev tools, hosting wind-down services. | Advertising | V1 |
| R5 | **Premium Data & API Subscriptions** | Analysts/VCs/journalists pay for full structured dataset, API access, and custom failure analytics dashboards ($49–$499/mo tiers). | SaaS | V1–V2 |
| R6 | **Display / Sponsored Placements** | Programmatic + direct ads on high-traffic graveyard pages; sponsored "Autopsy" articles (clearly labeled). | Advertising | V1 |
| R7 | **Acquirer Subscriptions** | Buyers pay monthly for early access to new Lifeboat listings, anonymous listings, and advanced search/alerts (e.g., $29–$99/mo). | SaaS | V2 |
| R8 | **M&A Advisory / Concierge** | Higher-touch brokered deals for larger acquisitions; success fee 3–5%. | Service | V2+ |

### 7.2 Strategic Rationale
- **R4/R5/R6 monetize traffic** even before marketplace liquidity exists — the Graveyard's SEO content funds the business while the Lifeboat two-sided market builds.
- **R1 is the long-term prize** but requires deal volume; deliberately deferred to V2 escrow flow.
- Classic two-sided marketplace sequencing: **content → audience → demand (buyers) → supply (sellers) → transactions**.

---

## 8. Business Rules & Policies (Key)

| ID | Rule |
|---|---|
| BR-01 | A project enters the Graveyard only with verifiable public evidence (official announcement, credible press). No fake deaths. |
| BR-02 | Lifeboat listings must be submitted by someone with authority to sell (owner or authorized rep); verified via domain/email ownership check. |
| BR-03 | Projects acquired via the Lifeboat and later revived are moved from "Graveyard-risk" to "Rescued" status — a positive outcome the platform actively promotes. |
| BR-04 | Platform is a venue/facilitator, not a broker of record in V1; all deals are buyer–seller direct. Legal disclaimer required. |
| BR-05 | Community submissions are moderated before publication (SLA: 48h). |
| BR-06 | Anonymous listings never expose founder identity without consent. |

---

## 9. Non-Functional Requirements

- **Performance:** Pages load < 2s; search results < 500ms.
- **SEO:** Server-side rendered pages, structured data, clean URLs per project.
- **Compliance:** GDPR/CCPA (analytics consent), clear editorial/sponsored labeling (FTC), DMCA process, terms covering listing accuracy disclaimers.
- **Content safety:** Moderation queue, defamation-safe language policy ("documented public facts + cited sources").
- **Availability:** 99.5% uptime target.

---

## 10. Risks & Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Legal exposure from documenting company failures | Medium | Cite public sources only; moderation; takedown process; neutral tone. |
| Marketplace chicken-and-egg (no buyers or no sellers) | High | Build Graveyard audience first (SEO/newsletter), then recruit sellers, then open to buyers. |
| Data quality / fake listings | Medium | Verification tier, ownership checks, community flagging. |
| Negative brand perception ("profiting from failure") | Medium | Frame as preservation + rescue; publish "Rescued" success stories; respectful memorial tone. |
| TechCrunch / incumbent adds same features | Medium | Move fast on structured data + marketplace; they archive but don't enable exits. |

---

## 11. Roadmap (High-Level)

| Phase | Duration | Deliverables |
|---|---|---|
| **Phase 1 — MVP (Graveyard)** | Months 1–3 | Tombstone pages, search/filter, submissions + moderation, stats dashboard, newsletter. Seed with 150–300 entries from public sources (TechCrunch AI graveyard, discontinued trackers). |
| **Phase 2 — Lifeboat Launch** | Months 4–6 | Seller listings, buyer browsing, private offers, watchlist alerts, featured listings (R2), verified badges (R3). |
| **Phase 3 — Monetization & Growth** | Months 7–12 | Newsletter sponsorships, premium data/API tiers, acquirer subscriptions, embeddable widgets, success-story PR. |
| **Phase 4 — Transactions** | Months 12+ | Escrow deal flow, success-fee model, M&A concierge, internationalization. |

---

## 12. Success Metrics

- Graveyard: entries published, verified-entry ratio, organic traffic, newsletter open rate (>40%).
- Lifeboat: listings created, time-to-first-offer, offers per listing, completed acquisitions, GMV.
- Revenue: MRR by stream; CAC vs. LTV for acquirer subscriptions.
- North Star: **total value of assets rescued** (GMV of completed acquisitions + audience reach of failure lessons).

---

## 13. Open Questions

1. Branding: keep "AI Graveyard" (memorable, matches TechCrunch's term) vs. a name emphasizing rescue/marketplace?
2. Should the Lifeboat allow non-AI tech projects, or stay AI-only for positioning?
3. Manual vs. automated (scraping + LLM-assisted) entry collection in Phase 1?
4. Jurisdiction/company structure for marketplace transaction fees (V2 escrow)?

---

## Appendix D — Technical Architecture (Django + PostgreSQL + Node.js on Docker)

### D1. Stack Overview & Rationale

| Layer | Technology | Why |
|---|---|---|
| Core API & Admin | **Django 5 + Django REST Framework** | Rapid CRUD for tombstones/listings, battle-tested auth/permissions, free Admin CMS (covers Epic 6 out of the box), mature ORM for the analytics dashboard queries. |
| Database | **PostgreSQL 16** | Single source of truth for both Django and Node services; full-text search (graveyard search, US-1.2), JSONB for flexible listing metrics, LISTEN/NOTIFY for real-time fan-out. |
| Realtime service | **Node.js 22 (Express + Socket.IO)** | Private messaging, offer notifications, live counters on the hero (WebSocket), and saved-search alert dispatch — event-driven workloads where Node excels. |
| Background jobs | **Celery + Redis** | Moderation SLA timers (US-2.2), newsletter sends (US-5.2), verification reminders, listing expiry (60-day rule, US-3.1). |
| Cache / Pub-Sub | **Redis 7** | Celery broker + cache + event bus between Django and Node (Django publishes `offer.new`, Node pushes to WebSockets). |
| Reverse proxy | **Nginx** | Static/media serving, TLS termination, routes `/api/` → Django and `/ws/` → Node. |
| Frontend | Django templates + HTMX/Alpine (SSR) | Meets the SEO requirement (P-03) without a SPA; progressive enhancement for reactions, offers, water-level animations. |
| Env | **Docker Compose** | One-command local dev and single-host deploy; every service containerized from day 1. |

### D2. Service Topology

```
                        +------------------+
   Browser  ----------> |  nginx :80/:443  |
                        +--------+---------+
                     /api/    |      /ws/  static
                  +-----------+    +-----------+
                  v                v
          +--------------+  +--------------+
          | django (web) |  | node(realtime)|
          | gunicorn :8000|  | socket.io :3001|
          +------+-------+  +------+-------+
                 |                 |
                 |   +----------+  |
                 |   | redis :6379  |  (pub/sub + cache + broker)
                 |   +------+-------+
                 |          |
          +------v----------v------+
          |  postgres :5432        |
          +------------------------+
                 ^
          +------+------+
          | celery worker|  (emails, newsletter, expiry timers)
          +-------------+
```

- Django owns all writes. Node reads Postgres (read-only creds) for live counters and subscribes to Redis channels for push events — avoids dual-write problems.
- Event flow (offer submitted): Django validates + persists → publishes `offer.new` to Redis → Node receives → Socket.IO emits to the seller's room → Celery sends the email notification.

### D3. Repository Layout

```
graveyard/
├── docker-compose.yml
├── docker-compose.prod.yml        # gunicorn workers, TLS, no dev mounts
├── .env.example
├── nginx/
│   └── default.conf
├── backend/                       # Django project
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── manage.py
│   ├── config/                    # settings/ (base, dev, prod), urls, celery
│   └── apps/
│       ├── core/                  # shared utils, pagination, cloudinary/media
│       ├── accounts/              # US-5.1 — roles: reader/founder/buyer
│       ├── graveyard/             # Epics 1 & 2 — Grave, CauseOfDeath, Source,
│       │                          #   Submission, Reaction, Comment, Status enum
│       ├── lifeboat/              # Epics 3 & 4 — Listing, AssetType, Offer,
│       │                          #   MessageThread, Verification, Watchlist/SavedSearch
│       ├── analytics/             # US-1.4, C8 — stats endpoints, embed widget
│       └── notify/                # notification prefs, digests
├── realtime/                      # Node service
│   ├── Dockerfile
│   ├── package.json
│   └── src/
│       ├── server.js              # Express + Socket.IO + healthcheck
│       ├── redis-sub.js           # subscribe offer.new, listing.new, grave.new
│       ├── rooms.js               # per-user rooms, listing rooms
│       └── counters.js            # cached live counters (PG polling + invalidation)
└── db/
    └── init/                      # 00-create-readonly-role.sql (for Node)
```

### D4. docker-compose.yml (dev skeleton)

```yaml
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: graveyard
      POSTGRES_USER: graveyard
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - pgdata:/var/lib/postgresql/data
      - ./db/init:/docker-entrypoint-initdb.d   # creates 'realtime_ro' role
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U graveyard"]
      interval: 5s
      retries: 10

  redis:
    image: redis:7-alpine
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s

  web:
    build: ./backend
    command: python manage.py runserver 0.0.0.0:8000   # prod: gunicorn
    volumes:
      - ./backend:/app
    environment: &web-env
      DATABASE_URL: postgres://graveyard:${DB_PASSWORD}@db:5432/graveyard
      REDIS_URL: redis://redis:6379/0
      DJANGO_SECRET_KEY: ${DJANGO_SECRET_KEY}
      DJANGO_DEBUG: "1"
    depends_on:
      db: { condition: service_healthy }
      redis: { condition: service_healthy }

  worker:
    build: ./backend
    command: celery -A config worker -l info
    volumes:
      - ./backend:/app
    environment: *web-env               # same env as web
    depends_on: [web, redis]

  realtime:
    build: ./realtime
    environment:
      DATABASE_URL: postgres://realtime_ro:${DB_PASSWORD}@db:5432/graveyard
      REDIS_URL: redis://redis:6379/1
      PORT: "3001"
    depends_on:
      db: { condition: service_healthy }
      redis: { condition: service_healthy }

  nginx:
    image: nginx:alpine
    ports: ["80:80"]
    volumes:
      - ./nginx/default.conf:/etc/nginx/conf.d/default.conf:ro
      - ./backend/media:/srv/media:ro
    depends_on: [web, realtime]

volumes:
  pgdata:
```

### D5. Key Django Models (mapping to Epics)

| Model | Key fields | Source |
|---|---|---|
| `Grave` | name, slug, status (DEAD/PIVOTED/ABSORBED/DELAYED/ROLLBACK/UNCONFIRMED), born_on, died_on, funding_raised, category FK, cause FK, narrative (HTML), capital_buried | G-01, G-08, US-2.3 |
| `Source` | grave FK, url, title, published_on | BR-01 |
| `Submission` | submitter FK, payload JSONB, status (PENDING/APPROVED/REJECTED), moderator FK, reject_reason, created_at (SLA timer) | US-2.1/2.2 |
| `Listing` | seller FK, title, category FK, asset_types (ArrayField), pricing_mode (FIXED/OFFER/GIVEAWAY), price, metrics JSONB (mrr, users, churn, traffic_trend), runway_months, urgency_score (0–100, computed → water level), stealth bool, verified bool, expires_at, status (ACTIVE/UNDER_AGREEMENT/SOLD/EXPIRED) | L-01…L-05 |
| `Verification` | listing FK, evidence files, admin FK, verified_fields, decided_at | US-6.2 |
| `Offer` | listing FK, buyer FK, amount, message, status (SENT/ACCEPTED/COUNTERED/DECLINED), thread FK | US-3.6, US-4.2 |
| `MessageThread` / `Message` | participants M2M, encrypted-at-rest optional, unread counts | L-04 |
| `SavedSearch` | user FK, filters JSONB, alert_channel (INSTANT/DIGEST) | US-4.3 |
| `Reaction` / `Comment` | user FK, grave FK, unique_together (candle per user) | US-1.5 |

### D6. API Surface (summary)

| Endpoint | Service | Notes |
|---|---|---|
| `GET/POST /api/graves/`, `GET /api/graves/{slug}/` | Django | filters = status, category, cause, year, funding; full-text `?q=` |
| `POST /api/graves/submit/` | Django | throttled (5/day/user), requires evidence URL |
| `GET /api/stats/` | Django | cached 5 min in Redis; powers C8 + embed widget |
| `GET/POST /api/listings/`, `GET /api/listings/{id}/` | Django | stealth listings mask seller + name for non-offering users |
| `POST /api/listings/{id}/offers/` | Django | emits `offer.new` to Redis |
| `GET/WS /ws/` | Node | rooms: `user:{id}`, `listing:{id}`, `global:counters` |
| `GET /healthz` | all | for Docker healthchecks |

### D7. Environments & Ops

- **Dev:** `docker compose up` — Django runserver with autoreload, Node with `nodemon`, source mounted.
- **CI:** lint (ruff, eslint) → test (pytest-django, jest) → build images → `docker compose -f docker-compose.yml -f docker-compose.prod.yml config` validation.
- **Prod (Phase 1):** single host, Compose with gunicorn (3 workers), `web` replicas scale later; Postgres daily `pg_dump` to object storage; media on S3-compatible storage.
- **Prod (later):** move to Swarm/K8s or managed Postgres when marketplace escrow (V2) lands — no architecture change needed since services are already discrete containers behind nginx.

### D8. Traceability — Stack ↔ Requirements

| Requirement | Covered by |
|---|---|
| Tombstone SEO (P-03) | Django SSR + `schema.org` microdata in templates |
| Moderation SLA 48h (BR-05) | Celery beat reminder + queue aging in Django Admin |
| Private offers (US-3.6/4.2) | Django API + Redis pub/sub + Node Socket.IO rooms |
| Live counters (C1 hero) | Node `counters.js` + `global:counters` room |
| Verified badges (L-06) | `Verification` model + admin workflow |
| Listing expiry 60 days (US-3.1) | Celery beat daily job |
| Widget embeds (P-06) | Cached `/api/stats/` + iframe/JS snippet |

---

## Appendix A — Seed Entries (from TechCrunch, Oct 2026)

Relay (workflow automation, shut down Aug 2026) · Character.ai (bankruptcy, Oct 2026) · Sora (OpenAI video platform, shut down Mar 2026) · ChatGPT Atlas (browser, discontinued Aug 2026) · OpenAI "super app" redesign (rolled back) · Apple Siri AI (delayed ~2 years; $250M settlement) · Microsoft Recall (delayed, privacy backlash) · Notion Mail (shutting down) · Humane AI Pin ($230M raised; assets to HP for $116M) · Rabbit R1 (pivot) · Huxe (audio app, shut down May 2026) · Yupp (model comparison, shut down Mar 2026) · Figgs AI (2023–2024).

---

## Appendix B — User Stories & Acceptance Criteria

Format: **ID** — *As a [persona], I want [goal], so that [benefit].*
Priority: Must (M) / Should (S) / Could (C). Acceptance criteria in Given/When/Then form.

### Epic 1 — Graveyard Browsing (P1: Historian)

**US-1.1 (M)** — *As a visitor, I want to browse a chronological feed of dead AI projects, so that I can see what recently failed.*
- Given I'm on the home page, when the page loads, then I see the 10 most recently published tombstones, each showing logo, name, category, "died" date, and cause-of-death tag.
- Given a new entry is published, when it goes live, then it appears at the top of the feed with a "New" marker for 72 hours.

**US-1.2 (M)** — *As a visitor, I want to search and filter the graveyard, so that I can find projects by category, funding size, cause of death, or year.*
- Given I'm on the Graveyard list page, when I apply the filter "Cause: Competition" + "Year: 2026", then only matching tombstones are shown and the result count updates.
- Given my search returns no results, when the results render, then I see suggested similar entries and an option to submit the missing project.

**US-1.3 (M)** — *As a visitor, I want to open a project's tombstone page, so that I can learn its full story — lifespan, funding, cause of death, and lessons.*
- Given I open a tombstone, when the page renders, then I see: name, logo, one-line summary, Born/Died dates, status badge (Dead / Pivoted / Absorbed / Delayed / Rollback), funding raised, category, cause-of-death category, full narrative (with cited sources), and related entries.
- Given the entry is "Absorbed" or "Pivoted", when I view it, then the page links to the parent/successor project.

**US-1.4 (S)** — *As an analyst, I want an aggregated statistics dashboard, so that I can spot failure trends without reading every entry.*
- Given I open the Stats page, when it loads, then I see: deaths per quarter (chart), top causes of death (bar), total capital buried (counter), biggest graves by funding (table), all filterable by category and year.

**US-1.5 (S)** — *As a returning visitor, I want to leave a reaction or comment on a tombstone, so that I can memorialize or discuss the project.*
- Given I'm logged in, when I click the 🕯 candle icon, then the counter increments and my reaction is stored (one per user per entry).
- Given I'm not logged in, when I try to comment, then I'm prompted to sign in.

**US-1.6 (C)** — *As a blogger, I want to embed a graveyard stats widget, so that my readers see live failure data.*
- Given I paste the embed snippet, when my page loads, then the widget renders current stats with a backlink to the platform.

### Epic 2 — Submission & Moderation (P1: Historian / P4: Curator)

**US-2.1 (M)** — *As a visitor, I want to submit a dead project with source links, so that the archive stays complete.*
- Given I'm on the submission form, when I complete required fields (name, URL, category, shutdown evidence link) and submit, then I see a confirmation and the entry enters the moderation queue.
- Given I omit the evidence link, when I submit, then validation blocks me with the message "A verifiable source is required."

**US-2.2 (M)** — *As a moderator, I want a review queue with source links, so that I can verify or reject submissions before publication.*
- Given I open the admin queue, when a submission has an invalid or paywalled unverifiable source, when I click Reject with reason, then the submitter is notified and the entry is not published.
- Given I approve an entry, when it publishes, then it appears in the public feed and the submitter receives credit on the tombstone ("Submitted by @user").

**US-2.3 (S)** — *As a moderator, I want to flag entries "Under Review", so that disputed deaths (e.g., rumored shutdowns) aren't presented as fact.*
- Given a rumor circulates about a project shutting down, when I mark the entry "Unconfirmed", then the public page shows a warning banner and the entry is excluded from the Stats dashboard.

### Epic 3 — Lifeboat: Selling (P2: Survivor)

**US-3.1 (M)** — *As a founder, I want to list my struggling project with full details, so that buyers can evaluate it.*
- Given I'm verified as the project owner, when I complete the listing wizard (basics → metrics → assets for sale → pricing → review), then my listing goes live with status "Active" for 60 days (renewable).
- Given I claim a domain, when I create the listing, then I must verify ownership via DNS TXT record or email on the domain before publishing.

**US-3.2 (M)** — *As a founder, I want to specify what exactly is for sale, so that I'm not forced to sell everything.*
- Given I'm in the listing wizard, when I select asset types (whole product / codebase / domain+brand / user base / customer list / team hire), then only selected assets appear on the public listing and the rest are excluded from any deal.

**US-3.3 (M)** — *As a founder, I want to choose my pricing mode, so that I control how offers come in.*
- Given I reach the pricing step, when I select Fixed Price ($X), Make Offer, or Giveaway (free to a good home), then the listing displays the corresponding badge and the buyer CTA matches (Buy / Make Offer / Apply to Adopt).

**US-3.4 (S)** — *As a founder, I want to disclose distress signals (runway, traffic decline), so that serious buyers understand the urgency.*
- Given I enter runway (e.g., "4 months") and optionally connect analytics screenshots, when the listing is published, then a "water level" urgency indicator renders (e.g., 70% submerged) based on disclosed signals.
- Given I'd rather not disclose publicly, when I mark signals private, then they're revealed only to buyers who submit an offer.

**US-3.5 (S)** — *As a founder, I want an anonymous ("stealth") listing, so that I can test acquisition interest without publicly signaling distress.*
- Given I choose Stealth mode, when the listing publishes, then it hides my name and brand ("Stealth AI SaaS — $8K MRR, dev-tools category") and interested buyers message me through the platform blind.

**US-3.6 (M)** — *As a founder, I want to receive and respond to private offers, so that I can negotiate without exposing the conversation publicly.*
- Given a buyer submits an offer, when it arrives, then I get an email + in-app notification with amount, message, and buyer profile, and Accept / Decline / Counter buttons.
- Given I accept an offer, when I confirm, then the listing status changes to "Under Agreement" (hidden from browse) and both parties receive a deal checklist (due-diligence docs, asset transfer steps).

### Epic 4 — Lifeboat: Buying (P3: Salvager)

**US-4.1 (M)** — *As a buyer, I want to browse and filter Lifeboat listings, so that I find rescue targets matching my criteria.*
- Given I'm on the Lifeboat page, when I filter by "min $5K MRR" + "price under $50K" + "tech stack: Python", then only matching listings render, sorted by newest or urgency.
- Given a listing has a Verified badge, when I view the card, then the badge is visible and links to what was verified (analytics, revenue) and when.

**US-4.2 (M)** — *As a buyer, I want to contact a seller or submit an offer privately, so that I can start a deal.*
- Given I'm logged in, when I submit an offer with amount and message, then the seller is notified and a private thread opens between us.
- Given I'm not logged in, when I click "Make Offer", then I'm prompted to create a buyer account first.

**US-4.3 (S)** — *As a buyer, I want saved searches and alerts, so that I'm notified the moment a matching project lists itself.*
- Given I save a search (category + min MRR + max price), when a new listing matches, then I receive an email alert within 1 hour.
- Given I'm a premium subscriber, when I have saved searches, then I receive match alerts before free users (early access window).

**US-4.4 (S)** — *As a buyer, I want a due-diligence view per listing, so that I can evaluate risk quickly.*
- Given I open a listing detail page, when it renders, then I see: seller pitch, metrics (with verification status), traffic/revenue trend charts if disclosed, tech stack, what's included, asking mode, days on market, and seller response-time rating.

### Epic 5 — Accounts, Notifications & Newsletter

**US-5.1 (M)** — *As a user, I want to sign up with email or SSO, so that I can submit, list, or offer.*
- Given I sign up, when I choose a role (Reader / Founder / Buyer — multi-selectable), then my profile and permissions reflect the selection; Reader is default.

**US-5.2 (M)** — *As a subscriber, I want the weekly newsletter, so that I get "Who Died This Week" + "Sinking Ships to Save" in one digest.*
- Given I subscribe, when Friday 09:00 (user timezone) arrives, then I receive the digest with new tombstones, trending Lifeboat listings, and one featured post-mortem.
- Given I unsubscribe, when I click the link, then I'm removed within 24h (one-click, no login required — GDPR/CTD compliance).

**US-5.3 (S)** — *As a user, I want granular notification settings, so that I control what emails I get.*
- Given I open notification settings, when I toggle categories (watchlist matches, offers received, offer responses, replies, digest), then only enabled categories are sent.

### Epic 6 — Admin & Trust (P4: Curator)

**US-6.1 (M)** — *As an admin, I want a CMS to create/edit tombstones and manage listings, so that data quality stays high.*
- Given I edit a published tombstone, when I save, then the change logs with timestamp and editor name (audit trail) and the public page updates.

**US-6.2 (M)** — *As an admin, I want to verify listing metrics, so that buyers can trust "Verified" badges.*
- Given a seller requests verification, when I review their evidence (analytics/statement screenshots, live access), then I can approve (badge applied, dated) or reject (reason sent to seller).

**US-6.3 (S)** — *As an admin, I want community flagging on entries and listings, so that abuse and inaccuracies surface fast.*
- Given a user flags content, when 3 flags accumulate or 1 admin flag occurs, then the content is auto-hidden pending review.

---

## Appendix C — Wireframe Descriptions (Lo-Fi)

### C1. Home Page

```
+--------------------------------------------------------------------------+
|  [Logo] AI GRAVEYARD          Graveyard | Lifeboat | Stats | [Search]     |
|                                        Sign in / [Submit a Death]        |
+--------------------------------------------------------------------------+
|  HERO: "42% of AI projects die. We keep the receipts."                   |
|  [ 1,247 buried  |  38 sinking ships  |  $4.2B capital burned  ]  <- live counters
+------------------------------------+-------------------------------------+
|  RIP THIS MONTH (feed)             |  SINKING SHIPS (Lifeboat preview)  |
|  +------------------------------+  |  +-------------------------------+ |
|  | [logo] Character.ai   DEAD   |  |  | Stealth AI SaaS   $8K MRR    | |
|  | Chatbots | Oct 2026 | Legal  |  |  | dev-tools | ~70% submerged   | |
|  +------------------------------+  |  | [View listing]               | |
|  | [logo] Sora           DEAD   |  |  +-------------------------------+ |
|  | Video    | Mar 2026 | Cost   |  |  | AI Notes App  Make Offer     | |
|  +------------------------------+  |  | productivity | ~40% submerged | |
|  | ... (10 cards)   [See all]   |  |  +-------------------------------+ |
+------------------------------------+-------------------------------------+
|  TRENDING AUTOPSIES (3 editorial cards)                                  |
+--------------------------------------------------------------------------+
|  NEWSLETTER: "Who Died This Week"  [email] [Subscribe]                    |
+--------------------------------------------------------------------------+
|  Footer: About | API | Press | Legal | Embed widget                       |
+--------------------------------------------------------------------------+
```

**Notes:** Hero counters animate on load (shareable moment). Dual feed above the fold introduces both pillars immediately.

### C2. Graveyard List Page

```
+--------------------------------------------------------------------------+
|  THE GRAVEYARD                                [Submit a Death]            |
+--------------------------------------------------------------------------+
|  FILTERS:  [Status v] [Category v] [Cause of death v] [Year v] [Funding v]
|            Sort: [Newest v]                    1,247 results             |
+--------------------------------------------------------------------------+
|  +----------------------------------------------------------------------+
|  | [logo]  HUXE                      [ DEAD ]     May 2026              |
|  | AI audio app by ex-NotebookLM devs | Audio      Cause: Competition   |
|  | $4.2M raised | 2024 – 2026 (2 yrs)               3 yrs... [Read]     |
|  +----------------------------------------------------------------------+
|  | [logo]  CHATGPT ATLAS            [ ABSORBED ]   Aug 2026             |
|  | Standalone AI browser by OpenAI   | Browser     Cause: Consolidation |
|  +----------------------------------------------------------------------+
|  | [logo]  APPLE SIRI AI            [ DELAYED ]    Live Oct 2026        |
|  +----------------------------------------------------------------------+
|       ... pagination / infinite scroll ...                               |
+--------------------------------------------------------------------------+
```

### C3. Tombstone Detail Page

```
+--------------------------------------------------------------------------+
|  <- Back to Graveyard                                                    |
+--------------------------------------------------------------------------+
|  [logo]   CHARACTER.AI            [ DEAD ]  [ Bankruptcy ]              |
|  "Custom AI character chat — raised $150M at a $1B valuation"           |
+--------------------------------------------------------------------------+
|  Born: 2021        Died: Oct 2026        Lifespan: 5 years              |
|  Funding: $150M+   Category: Chatbots    Region: US                     |
+--------------------------------------------------------------------------+
|  THE AUTOPSY (narrative, 400-800 words)                                  |
|  Timeline: 2021 founded > 2023 $150M raise > 2024 Google $2.7B          |
|  license & founders exit > 2025 lawsuits > 2026 bankruptcy filing       |
|  Sources: [1] TechCrunch [2] Court filing [3] Official statement        |
+--------------------------------------------------------------------------+
|  WHAT WE LEARNED  (2-3 bullet takeaways)                                 |
+--------------------------------------------------------------------------+
|  Related graves: [Figgs AI] [Humane AI Pin]   Related Lifeboat: —        |
+--------------------------------------------------------------------------+
|  🕯 2,341 mourners   [Leave a candle]    Comments (128) [Add comment]   |
+--------------------------------------------------------------------------+
```

**Notes:** Status badge and cause tag drive filter consistency. "Related Lifeboat" cross-links when a successor/rescue exists.

### C4. Lifeboat Browse Page

```
+--------------------------------------------------------------------------+
|  THE LIFEBOARD — rescue a project          [List your project]           |
|  "These ships are sinking. You can save one."                            |
+--------------------------------------------------------------------------+
|  FILTERS: [Category v] [Asset type v] [Price range v]                   |
|           [Min MRR v] [Tech stack v] [Urgency v] [Verified only []]     |
+-----------------------------+--------------------------------------------+
|  +------------------------+ |  +------------------------+                |
|  | STEALTH AI SaaS        | |  | AI NOTES APP           |                |
|  | dev-tools | $8K MRR    | |  | productivity | 12K users|               |
|  |  # # # # ~~~ 70%       | |  # # ~~~~~~~~ 40%          |               |
|  |  [VERIFIED]  $45K      | |  Make Offer                |                |
|  +------------------------+ |  +------------------------+                |
|  ... card grid (urgency water-level bar under each card) ...             |
+--------------------------------------------------------------------------+
|  Success story banner: "Read how X was rescued and hit $20K MRR"        |
+--------------------------------------------------------------------------+
```

**Notes:** "Water level" bar = urgency indicator (blue fill rising over the card bottom). Verified badge is visually distinct.

### C5. Lifeboat Listing Detail Page

```
+--------------------------------------------------------------------------+
|  <- Back to Lifeboat                          [Report listing]           |
+--------------------------------------------------------------------------+
|  STEALTH AI SaaS                            [VERIFIED]  Listed 12d ago   |
|  dev-tools | Whole product for sale | $45K fixed                         |
+--------------------------------------------------------------------------+
|  METRICS (Verified 2026-10-20)    |  THE PITCH                           |
|  MRR: $8,000   (v)               |  Seller narrative, why it's sinking, |
|  Users: 3,400   (v)              |  what's working, what's not          |
|  Churn: 6%/mo   (v)              |---------------------------------------|
|  Traffic: -35% / 6mo             |  WHAT'S INCLUDED                      |
|                                  |  [x] Codebase [x] Domain+brand       |
|  RUNWAY: ~4 months               |  [x] User base [ ] Customer list     |
|  # # # # ~~~ 70% submerged       |  [ ] Team hire                        |
+--------------------------------------------------------------------------+
|  TECH: Python / Next.js / Postgres   |  SELLER: @founder (responds ~4h)  |
+--------------------------------------------------------------------------+
|        [ Message Seller ]      [ Make Offer: $____ __ ]                  |
|  Similar listings: [card] [card] [card]                                  |
+--------------------------------------------------------------------------+
```

### C6. Listing Wizard (Seller) — 5 Steps

```
  Step 1 Basics      Step 2 Metrics      Step 3 Assets      Step 4 Pricing   Step 5 Review
  [======------------|-------------------|------------------|-----------------]
  +-------------------------------------------------------------------+
  |  1. Project name, URL, category, one-line pitch                   |
  |     -> Domain ownership verification (DNS TXT / email) [VERIFY]   |
  |  2. MRR, users, churn, traffic trend, runway                      |
  |     -> Optional: upload analytics screenshots for [VERIFIED]      |
  |     -> Optional: mark metrics "private until offer"               |
  |  3. Assets for sale: checkboxes (product/code/domain/             |
  |     users/customers/team) + anonymous "Stealth mode" toggle       |
  |  4. Pricing mode: ( ) Fixed $___  ( ) Make Offer  ( ) Giveaway    |
  |  5. Preview public card -> [Publish] (60 days, renewable)         |
  +-------------------------------------------------------------------+
```

### C7. Submit a Death (Public Form)

```
  +-----------------------------------------------+
  |  REPORT A DEATH                                |
  |  Project name*        [_______________]        |
  |  URL                  [_______________]        |
  |  Category*            [drop-down v]            |
  |  Status*              ( ) Dead ( ) Pivoted     |
  |                       ( ) Absorbed ( ) Delayed |
  |  Shutdown date*       [____-__-__]             |
  |  Evidence link*       [https://________]       |
  |  Additional context   [textarea]               |
  |             [ Submit for review ]              |
  |  "Verified by moderators within 48h.          |
  |   You'll be credited on the tombstone."       |
  +-----------------------------------------------+
```

### C8. Stats Dashboard

```
+--------------------------------------------------------------------------+
|  GRAYARD ANALYTICS            Filters: [Category v] [Year v] [Export]    |
+--------------------------------------------------------------------------+
|  DEATHS PER QUARTER (line chart)      |  TOP CAUSES OF DEATH (bars)     |
|      /\    /\                         |  Competition       ##########   |
|   /\/  \/\  \/\/\                     |  No PMF            ########     |
|  2024      2026                       |  Funding           #######      |
|                                       |  Legal/Reg.        #####        |
+---------------------------------------+---------------------------------+
|  TOTAL CAPITAL BURIED: $4.2B          |  BIGGEST GRAVES (table)         |
|  AVG LIFESPAN: 2.3 yrs                |  1. Character.ai   $150M+       |
|                                       |  2. Humane AI Pin  $230M        |
|  [Embed this chart]                   |  3. ...                          |
+--------------------------------------------------------------------------+
```

### C9. Global Navigation & IA (Site Map)

```
                       AI Graveyard
                       /     |     \
              GRAVEYARD  LIFEBOAT  STATS
              /     \       |          \
        Browse   Submit  Browse      Charts
          |      a Death  |  List       + API/Export
        Tombstone       Offer flow   (premium)
          |             |
       Comments/     Seller wizard
       Reactions
                       + NEWSLETTER (cross-cutting)
                       + ACCOUNT: Reader / Founder / Buyer roles
                       + ADMIN: queue, CMS, verification, flags
```

---

