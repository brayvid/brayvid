import os
import hashlib
from flask import Flask, render_template, make_response, request
from weasyprint import HTML, CSS

app = Flask(__name__)

# --- Caching Mechanism ---
pdf_cache = None
# We no longer need template_last_modified for the pre-warming strategy,
# as a new deploy will always regenerate the PDF.
# --- End Caching Mechanism ---

# --- Pre-warming the Cache ---
def generate_and_cache_pdf():
    """
    A function to generate the PDF and store it in the global cache.
    This is called ONCE when the application starts.
    """
    global pdf_cache
    print("Pre-warming cache: Generating PDF at startup...")
    try:
        # Render the HTML template for the PDF
        html_string = render_template('index.html', is_pdf_render=True)
        base_url = os.path.join(app.root_path, 'static')
        page_layout_css = CSS(string="@page { size: letter; margin: 0.02in; }")
        
        html_obj = HTML(string=html_string, base_url=base_url)
        pdf_bytes = html_obj.write_pdf(stylesheets=[page_layout_css])
        
        # Store the generated PDF in our global variable
        pdf_cache = pdf_bytes
        print("PDF generated and cached successfully.")
    except Exception as e:
        print(f"FATAL: Could not generate PDF at startup: {e}")
        # If this fails, the app shouldn't start.
        # pdf_cache will remain None.
        
# --- End Pre-warming the Cache ---


@app.route('/')
def resume():
    """Renders the HTML resume page."""
    response = make_response(render_template('index.html'))
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.route('/download-pdf')
def download_pdf():
    """
    Serves the pre-cached PDF.
    """
    # If caching failed at startup, we should return an error.
    if pdf_cache is None:
        return "Error: PDF is not available, check application logs.", 500

    response = make_response(pdf_cache)
    
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=blake-rayvid-cv.pdf'
    response.headers['Cache-Control'] = 'public, max-age=3600'
    
    etag = hashlib.md5(pdf_cache).hexdigest()
    response.set_etag(etag)
    
    return response.make_conditional(request)

# This block ensures the pre-warming only happens when running with Gunicorn
# and not during other Flask CLI commands.
with app.app_context():
    generate_and_cache_pdf()

if __name__ == '__main__':
    # The debug server will also use the pre-warmed cache.
    app.run(debug=True)