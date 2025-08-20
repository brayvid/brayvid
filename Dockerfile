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

# --- Install Custom Fonts System-Wide ---
# Create a standard directory for custom TrueType fonts
RUN mkdir -p /usr/local/share/fonts/truetype/
# Copy your font files from your project's static/src directory into it
COPY static/src/*.ttf /usr/local/share/fonts/truetype/
# Rebuild the system's font cache. The -v flag is for verbose output.
RUN fc-cache -f -v
# --- End Font Installation ---

# Copy all application files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# --- Build-Time Step: Generate the PDF ---
# This will now run in an environment where the 'bka' font is installed
RUN python generate_pdf.py

# --- Runtime Step: Define the command to start the server ---
CMD gunicorn --bind=0.0.0.0:$PORT --workers=2 --timeout=120 app:app