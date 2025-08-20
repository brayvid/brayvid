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
workers = 2
timeout = 180
# NEW: Give workers a long time to boot, as they wait for the master process.
worker_boot_timeout = 240