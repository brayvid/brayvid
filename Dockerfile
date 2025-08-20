# Use a supported Python slim image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install system dependencies for WeasyPrint AND font management tools
RUN apt-get update && apt-get install -y \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libpangoft2-1.0-0 \
    libcairo2 \
    libgdk-pixbuf-xlib-2.0-0 \
    fontconfig \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# --- Font Installation and DIAGNOSTICS ---
# Create a directory for custom fonts
RUN mkdir -p /usr/local/share/fonts/truetype/
# Copy your font files into that directory
COPY static/src/*.ttf /usr/local/share/fonts/truetype/
# Copy our custom fontconfig file to the system's config directory
COPY local.conf /etc/fonts/conf.d/50-local.conf
# Rebuild the font cache.
RUN fc-cache -f -v

# --- START OF DIAGNOSTIC COMMANDS ---
# 1. Verify that the font files were copied correctly
RUN echo "--- Verifying font files exist ---" && \
    ls -l /usr/local/share/fonts/truetype/

# 2. Verify that the fontconfig file was copied correctly
RUN echo "--- Verifying font config exists ---" && \
    ls -l /etc/fonts/conf.d/50-local.conf

# 3. Ask the system to list all fonts it knows about, and search for 'bka'
RUN echo "--- Searching system font cache for 'bka' ---" && \
    fc-list | grep -i "bka" || echo "Font 'bka' not found in fc-list"

# 4. Ask the system to inspect the font files directly and report their properties
RUN echo "--- Querying metadata for bka.ttf ---" && \
    fc-query /usr/local/share/fonts/truetype/bka.ttf
RUN echo "--- Querying metadata for bka-bold.ttf ---" && \
    fc-query /usr/local/share/fonts/truetype/bka-bold.ttf
# --- END OF DIAGNOSTIC COMMANDS ---

# Copy all application files (again, simple way to ensure everything is there)
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# --- Build-Time Step: Generate the PDF ---
RUN echo "--- Attempting to generate PDF ---" && \
    python generate_pdf.py

# --- Runtime Step: Define the command to start the server ---
CMD gunicorn --bind=0.0.0.0:$PORT --workers=2 --timeout=120 app:app