# gunicorn.conf.py
import os
import sys

# Remove the aggressive logging if you confirmed Gunicorn loads config
# sys.stdout.reconfigure(line_buffering=True)
# sys.stderr.reconfigure(line_buffering=True)
# print(f"Gunicorn config file loaded. PID: {os.getpid()}")
# print(f"Attempting to bind to 0.0.0.0:{os.environ.get('PORT', '8000 (default fallback used)')}")


# No need to import app or generate_and_cache_pdf here anymore,
# as the hook that uses them is gone.
# from app import app, generate_and_cache_pdf

# Server Hooks
# Remove or comment out the on_starting hook entirely
# def on_starting(server):
#     print("Gunicorn master process starting. on_starting hook executed.")
#     # This hook is no longer responsible for PDF generation
#     # with app.app_context():
#     #     generate_and_cache_pdf()
#     print("on_starting hook finished.")


# Gunicorn settings
bind = f"0.0.0.0:{os.environ.get('PORT', 8000)}"
workers = 2
timeout = 180
worker_boot_timeout = 240