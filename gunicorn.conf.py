# gunicorn.conf.py
import os
import sys # Import sys for unbuffered output

# Force immediate flushing of print statements for debugging
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

# This print statement should execute if Gunicorn starts Python at all
print(f"Gunicorn config file loaded. PID: {os.getpid()}")
print(f"Attempting to bind to 0.0.0.0:{os.environ.get('PORT', '8000 (default fallback used)')}")

# Temporarily comment out the app import to rule out issues during initial import of app.py
# from app import app, generate_and_cache_pdf

# Server Hooks
def on_starting(server):
    # This will print if the hook is successfully registered and called
    print("Gunicorn master process starting. on_starting hook executed.")
    # Temporarily disable the actual PDF generation to isolate the issue
    # with app.app_context():
    #     generate_and_cache_pdf()
    print("on_starting hook finished (PDF generation bypassed for now).")


# Gunicorn settings
bind = f"0.0.0.0:{os.environ.get('PORT', 8000)}"
workers = 2 # Keep workers at 2 for now
timeout = 180
worker_boot_timeout = 240