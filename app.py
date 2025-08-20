# app.py
import os
import hashlib
from flask import Flask, render_template, make_response, request
from weasyprint import HTML, CSS

app = Flask(__name__)

# Global variable to hold the cached PDF
pdf_cache = None

def generate_and_cache_pdf():
    """
    Generates the PDF and stores it in the global pdf_cache variable.
    This function will be called by our Gunicorn hook or for local dev.
    """
    global pdf_cache
    print("Pre-warming cache: Generating PDF at startup...")
    try:
        # We need to create a request context for url_for() to work.
        with app.test_request_context():
            html_string = render_template('index.html', is_pdf_render=True)
        
        base_url = os.path.join(app.root_path, 'static')
        page_layout_css = CSS(string="@page { size: letter; margin: 0.02in; }")
        
        html_obj = HTML(string=html_string, base_url=base_url)
        pdf_bytes = html_obj.write_pdf(stylesheets=[page_layout_css])
        
        pdf_cache = pdf_bytes
        print("PDF generated and cached successfully.")
    except Exception as e:
        print(f"FATAL: Could not generate PDF at startup: {e}")

@app.route('/')
def resume():
    """Renders the HTML resume page."""
    return render_template('index.html')

@app.route('/download-pdf')
def download_pdf():
    """Serves the pre-cached PDF."""
    if pdf_cache is None:
        return "Error: PDF is not available, check application logs for startup errors.", 500

    response = make_response(pdf_cache)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=blake-rayvid-cv.pdf'
    response.headers['Cache-Control'] = 'public, max-age=3600'
    
    etag = hashlib.md5(pdf_cache).hexdigest()
    response.set_etag(etag)
    
    return response.make_conditional(request)

@app.route('/health')
def health_check():
    """
    A simple healthcheck endpoint that returns a 200 OK.
    This is used by the platform to confirm the container is live.
    """
    return {"status": "ok"}, 200

if __name__ == '__main__':
    # For local development, we still need to trigger the generation.
    # The app_context is needed for app-level operations.
    with app.app_context():
        generate_and_cache_pdf()
    app.run(debug=True)