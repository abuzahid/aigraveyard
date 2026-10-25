"""Redis pub/sub bridge: Django publishes domain events, Node pushes them
over Socket.IO (see BA doc Appendix D2 — Django owns all writes)."""
import json
import logging

import redis

logger = logging.getLogger(__name__)

_pool = None


def _get_client():
    global _pool
    from django.conf import settings

    if _pool is None:
        _pool = redis.ConnectionPool.from_url(settings.CELERY_BROKER_URL)
    return redis.Redis(connection_pool=_pool)


def publish_event(channel: str, data: dict) -> None:
    try:
        _get_client().publish(channel, json.dumps(data))
    except Exception:
        # Never let a notification failure break the request.
        logger.exception("Failed to publish event on %s", channel)
