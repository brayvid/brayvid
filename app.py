# app.py
import os
import hashlib
from flask import Flask, render_template, make_response, send_from_directory, request

# Weasyprint, HTML, CSS are no longer needed for runtime
# from weasyprint import HTML, CSS

app = Flask(__name__)

# No global pdf_cache needed anymore

# The generate_and_cache_pdf function is no longer needed in app.py
# It is now part of the Dockerfile build process.
# def generate_and_cache_pdf():
#    ... (removed) ...

@app.route('/')
def resume():
    """Renders the HTML resume page."""
    return render_template('index.html')

@app.route('/download-pdf')
def download_pdf():
    """Serves the pre-generated PDF file."""
    # The PDF is now a static file within the Docker image at /app/blake-rayvid-cv.pdf
    # Use send_from_directory to serve it directly.
    
    # You might want to remove the ETag logic if send_from_directory handles it
    # or keep it for fine-grained control if performance demands.
    # For simplicity, send_from_directory is usually sufficient and handles headers.

    # Option 1: Simplest (recommended)
    return send_from_directory(
        app.root_path,
        'blake-rayvid-cv.pdf',
        mimetype='application/pdf',
        as_attachment=True,
        download_name='blake-rayvid-cv.pdf',
        last_modified=os.path.getmtime(os.path.join(app.root_path, 'blake-rayvid-cv.pdf')) # Optional, but good for caching
    )

    # Option 2: Manual (if send_from_directory doesn't meet needs, or for more control)
    # try:
    #     with open(os.path.join(app.root_path, 'blake-rayvid-cv.pdf'), 'rb') as f:
    #         pdf_bytes = f.read()
    #     response = make_response(pdf_bytes)
    #     response.headers['Content-Type'] = 'application/pdf'
    #     response.headers['Content-Disposition'] = 'attachment; filename=blake-rayvid-cv.pdf'
    #     response.headers['Cache-Control'] = 'public, max-age=3600'
    #     etag = hashlib.md5(pdf_bytes).hexdigest()
    #     response.set_etag(etag)
    #     return response.make_conditional(request)
    # except FileNotFoundError:
    #     return "Error: PDF not found. Build process might have failed.", 500

@app.route('/health')
def health_check():
    """
    A simple healthcheck endpoint that returns a 200 OK.
    This is used by the platform to confirm the container is live.
    """
    return {"status": "ok"}, 200

if __name__ == '__main__':
    # No pre-warming needed here. The PDF is assumed to exist after build.
    # For local testing, you'd need to manually run the Dockerfile build or
    # keep the old generate_and_cache_pdf call if you want to test PDF generation locally without Docker.
    # For now, let's assume the PDF exists locally from a build step.
    
    # If you want to test download-pdf route locally without docker build:
    # You'd need a mock blake-rayvid-cv.pdf file in your root for local testing.
    # Or keep the generate_and_cache_pdf() in __main__
    # For now, we'll keep it simple for deployment.
    app.run(debug=True)