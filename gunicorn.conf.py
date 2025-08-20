# gunicorn.conf.py
import os
from app import app, generate_and_cache_pdf

# We need to access the global pdf_cache from the app module
from app import pdf_cache

def on_starting(server):
    """
    Master Gunicorn process hook to pre-warm the cache.
    This runs ONCE before any worker processes are forked.
    """
    # --- TEMPORARY TEST ---
    # Instead of generating the real PDF, we'll just cache a dummy value.
    global pdf_cache
    print("Bypassing PDF generation for testing. Caching dummy value.")
    app.pdf_cache = b"This is a test PDF."
    print("Dummy value cached.")
    # with app.app_context():
    #     generate_and_cache_pdf()
    # --- END TEMPORARY TEST ---

# Gunicorn settings
bind = f"0.0.0.0:{os.environ.get('PORT', 8000)}"
workers = 2 # Keep this at 2
timeout = 180