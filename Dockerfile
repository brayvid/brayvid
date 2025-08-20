# Dockerfile

FROM python:3.11-slim

# Install system dependencies required by WeasyPrint
RUN apt-get update && apt-get install -y \
    libpango-1.0-0 \
    libcairo2 \
    libgdk-pixbuf-xlib-2.0-0 \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy all application code including templates and static files
# This needs to happen BEFORE installing requirements and generating PDF
COPY . .

# Install Python dependencies AFTER copying source (for local deps if any)
RUN pip install --no-cache-dir -r requirements.txt

# --- NEW STEP: Generate PDF during build ---
# Use a temporary Flask app to generate the PDF
# We need Flask, its dependencies, and WeasyPrint to be installed first.
# This assumes your app.py is in /app and includes necessary render_template calls.
# We'll use a simplified app.py that doesn't rely on global cache for this step.

# Create a temporary script for PDF generation
# This script will be run ONCE during the build process
RUN python -c " \
import os; \
from flask import Flask, render_template; \
from weasyprint import HTML, CSS; \
\
app = Flask(__name__); \
\
# Manually create app context for url_for() to work during build \
with app.app_context(): \
    with app.test_request_context(): \
        html_string = render_template('index.html', is_pdf_render=True); \
\
base_url = os.path.join(app.root_path, 'static'); \
page_layout_css = CSS(string='@page { size: letter; margin: 0.02in; }'); \
\
html_obj = HTML(string=html_string, base_url=base_url); \
pdf_bytes = html_obj.write_pdf(stylesheets=[page_layout_css]); \
\
with open('blake-rayvid-cv.pdf', 'wb') as f: \
    f.write(pdf_bytes); \
"

# --- End NEW STEP ---

# The CMD is handled by your Procfile, Railway will use that.