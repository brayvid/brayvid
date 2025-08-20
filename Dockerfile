# Use a supported Python slim image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install system dependencies for WeasyPrint
RUN apt-get update && apt-get install -y \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libpangoft2-1.0-0 \
    libcairo2 \
    libgdk-pixbuf-xlib-2.0-0 \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Copy all application files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# --- Build-Time Step: Generate the PDF ---
RUN python generate_pdf.py

# --- Runtime Step: Define the command to start the server ---
# This command is executed by a shell, so $PORT is correctly expanded at runtime.
CMD gunicorn --bind=0.0.0.0:$PORT --workers=2 --timeout=120 app:app