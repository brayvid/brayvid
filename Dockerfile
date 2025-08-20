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
# Copy font files into that directory
COPY static/src/*.ttf /usr/local/share/fonts/truetype/
# Copy custom fontconfig file to the system's config directory
COPY local.conf /etc/fonts/conf.d/50-local.conf
# Rebuild the font cache.
RUN fc-cache -f -v

# Copy all application files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# --- Build-Time Step: Generate the PDF ---
RUN echo "--- Attempting to generate PDF ---" && \
    python generate_pdf.py

# --- Runtime Step: Define the command to start the server ---
CMD gunicorn --bind=0.0.0.0:$PORT --workers=2 --timeout=120 app:app