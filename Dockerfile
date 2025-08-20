# Use a supported Python slim image
FROM python:3.11-slim

# Set environment variables for better logging
ENV PYTHONUNBUFFERED=1
ENV GUNICORN_CMD_ARGS="--bind=0.0.0.0:$PORT --workers=2 --timeout=120"

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
# This runs our script to create the static PDF file inside the image
RUN python generate_pdf.py

# --- Runtime Step: Define the command to start the server ---
# This CMD line replaces the Procfile and gunicorn.conf.py
# Railway will automatically substitute the $PORT variable.
CMD ["gunicorn", "app:app"]