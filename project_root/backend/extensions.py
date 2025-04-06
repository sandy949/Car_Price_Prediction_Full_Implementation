"""
This module sets up basic request rate limiting using Flask-Limiter.
It restricts each client (based on IP address) to 100 requests per hour by default.
"""

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100 per hour"],  # fallback rate
)
