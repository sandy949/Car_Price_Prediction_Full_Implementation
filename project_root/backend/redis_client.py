# backend/redis_client.py

"""
redis_client.py

This module sets up and exposes a Redis client using environment variables.
It can be used throughout the application for caching, rate limiting,
or as a message broker for Celery.
"""

import redis
import os

redis_host = os.getenv("REDIS_HOST", "redis")
redis_port = int(os.getenv("REDIS_PORT", 6379))

redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
