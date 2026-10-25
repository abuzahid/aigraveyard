-- Read-only role for the Node realtime service.
-- Node NEVER writes; Django owns all writes (see BA doc Appendix D2).
CREATE ROLE realtime_ro LOGIN PASSWORD 'realtime_ro';
GRANT CONNECT ON DATABASE graveyard TO realtime_ro;
\c graveyard
GRANT USAGE ON SCHEMA public TO realtime_ro;
ALTER DEFAULT PRIVILEGES IN SCHEMA public FOR ROLE graveyard GRANT SELECT ON TABLES TO realtime_ro;
