# gunicorn.conf.py
import os
from app import app, generate_and_cache_pdf

# Server Hooks
def on_starting(server):
    """
    Master Gunicorn process hook to pre-warm the cache.
    This runs ONCE before any worker processes are forked.
    """
    with app.app_context():
        generate_and_cache_pdf()

# Gunicorn settings
bind = f"0.0.0.0:{os.environ.get('PORT', 8000)}"
workers = 3
# Increase the timeout, as PDF generation can be slow on startup.
timeout = 180