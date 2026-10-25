/**
 * AI Graveyard — realtime service (Node + Socket.IO).
 *
 * Rules of the architecture (BA doc Appendix D2):
 *  - Django owns ALL writes; this service only READS Postgres (realtime_ro role).
 *  - Push events arrive via Redis pub/sub channels published by Django:
 *      offer.new    -> pushed to the seller's private room  (US-3.6)
 *      listing.new  -> broadcast to counters watchers        (C4/L-03)
 *  - Token verification: DRF token is checked against Django /api/auth/me/.
 */
const express = require("express");
const http = require("http");
const { Server } = require("socket.io");
const Redis = require("ioredis");

const { getCounters, refresh: refreshCounters, startCounters } = require("./counters");

const PORT = process.env.PORT || 3001;
const DJANGO_API_URL = process.env.DJANGO_API_URL || "http://web:8000";

const app = express();
const server = http.createServer(app);
// Socket.IO served under /ws/ (nginx routes that prefix here)
const io = new Server(server, { cors: { origin: "*" }, path: "/ws/socket.io" });

// ---------- HTTP ----------
app.get(["/healthz", "/ws/healthz"], (_req, res) => res.json({ ok: true }));
app.get(["/counters", "/ws/counters"], (_req, res) => res.json(getCounters()));

// ---------- Token verification ----------
async function verifyToken(token) {
  try {
    const res = await fetch(`${DJANGO_API_URL}/api/auth/me/`, {
      headers: { Authorization: `Token ${token}` },
    });
    if (!res.ok) return null;
    const user = await res.json();
    return user.id || null;
  } catch {
    return null;
  }
}

// ---------- Socket.IO ----------
io.use(async (socket, next) => {
  const token = socket.handshake.auth && socket.handshake.auth.token;
  if (token) {
    const userId = await verifyToken(token);
    if (userId) socket.data.userId = userId; // invalid tokens still connect, anon-style
  }
  next();
});

io.on("connection", (socket) => {
  socket.join("global:counters");
  if (socket.data.userId) {
    socket.join(`user:${socket.data.userId}`);
    socket.emit("counters", getCounters());
  }
});

// ---------- Redis pub/sub fan-out ----------
const sub = new Redis(process.env.REDIS_URL || "redis://redis:6379/1");
sub.psubscribe("*");

sub.on("pmessage", (_pattern, channel, message) => {
  let payload;
  try {
    payload = JSON.parse(message);
  } catch {
    payload = { raw: message };
  }

  if (channel === "offer.new" && payload.seller_id) {
    io.to(`user:${payload.seller_id}`).emit("offer:new", payload);
  } else if (channel === "alert.match" && payload.user_id) {
    // US-4.3 — saved-search match push
    io.to(`user:${payload.user_id}`).emit("alert:match", payload);
  } else if (channel === "listing.new") {
    refreshCounters()
      .then((c) => io.to("global:counters").emit("counters:update", c))
      .catch(() => {});
  }
});

sub.on("error", (err) => console.error("[redis-sub]", err.message));

// ---------- Boot (retry until Postgres is migrated — first-boot race with web) ----------
function boot(attempt = 1) {
  startCounters()
    .then(() => {
      server.listen(PORT, () => console.log(`realtime service listening on :${PORT}`));
    })
    .catch((err) => {
      console.error(`[boot] db not ready (attempt ${attempt}): ${err.message} — retrying in 5s`);
      setTimeout(() => boot(attempt + 1), 5000);
    });
}
boot();
