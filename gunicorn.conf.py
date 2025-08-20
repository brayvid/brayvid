# gunicorn.conf.py
import os

# Gunicorn settings
bind = f"0.0.0.0:{os.environ.get('PORT', 8000)}"
workers = 2
timeout = 120 # Can be shorter now, as startup is fast