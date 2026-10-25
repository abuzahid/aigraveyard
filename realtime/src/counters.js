/**
 * Live hero counters (C1): buried count, sinking ships count.
 * Read-only against Postgres; refreshed every 30s and on listing.new events.
 */
const { Pool } = require("pg");

const pool = new Pool({ connectionString: process.env.DATABASE_URL });

let counters = { graves_buried: 0, sinking_ships: 0 };
let timer = null;

async function refresh() {
  const { rows } = await pool.query(`
    SELECT
      (SELECT COUNT(*) FROM graveyard_grave WHERE status = 'dead') AS graves_buried,
      (SELECT COUNT(*) FROM lifeboat_listing WHERE status = 'active') AS sinking_ships
  `);
  counters = {
    graves_buried: Number(rows[0].graves_buried || 0),
    sinking_ships: Number(rows[0].sinking_ships || 0),
  };
  return counters;
}

async function startCounters() {
  await refresh();
  timer = setInterval(() => {
    refresh().catch((err) => console.error("[counters]", err.message));
  }, 30_000);
  if (timer.unref) timer.unref();
  return counters;
}

function getCounters() {
  return counters;
}

module.exports = { startCounters, refresh, getCounters };
