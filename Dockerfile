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

# Copy all application code including templates and static files FIRST
# This ensures generate_pdf.py and index.html are present for the next step.
COPY . .

# Install Python dependencies AFTER copying source
RUN pip install --no-cache-dir -r requirements.txt

# --- NEW STEP: Generate PDF during build using the script ---
# This step runs the script that generates and saves the PDF.
RUN python generate_pdf.py

# --- End NEW STEP ---

# The CMD is handled by your Procfile, Railway will use that.