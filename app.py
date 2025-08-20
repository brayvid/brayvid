import os
import hashlib
from flask import Flask, render_template, make_response, request
from weasyprint import HTML, CSS

app = Flask(__name__)

# --- Caching Mechanism ---
# Global variables to hold the cached PDF and track the template's modification time.
pdf_cache = None
template_last_modified = 0
# --- End Caching Mechanism ---

@app.route('/')
def resume():
    """Renders the HTML resume page."""
    # This route is fast, but for consistency, we can also add caching headers here.
    response = make_response(render_template('index.html'))
    # Set a short cache time for the HTML page itself.
    response.headers['Cache-Control'] = 'public, max-age=600' # Cache for 10 minutes
    return response

@app.route('/download-pdf')
def download_pdf():
    """
    Generates and serves the PDF version of the resume, with caching.
    The PDF is regenerated only if the underlying HTML template has changed.
    """
    global pdf_cache, template_last_modified

    try:
        template_path = os.path.join(app.root_path, 'templates', 'index.html')
        current_mtime = os.path.getmtime(template_path)

        # Cache Invalidation Check:
        # If the template file has been modified since the last cache, regenerate the PDF.
        if current_mtime > template_last_modified:
            print("Cache miss: Template has changed. Regenerating PDF...")
            
            # Render the HTML template, passing a flag to hide the download button.
            html_string = render_template('index.html', is_pdf_render=True)

            # The base_url is crucial for WeasyPrint to find static files like your fonts.
            base_url = os.path.join(app.root_path, 'static')
            
            # Define the PDF page layout.
            page_layout_css = CSS(string="@page { size: letter; margin: 0.02in; }")
            
            html_obj = HTML(string=html_string, base_url=base_url)
            
            # Generate the PDF bytes and store them in our in-memory cache.
            pdf_bytes = html_obj.write_pdf(stylesheets=[page_layout_css])
            pdf_cache = pdf_bytes
            
            # Update the last modified time.
            template_last_modified = current_mtime
        else:
            print("Cache hit: Serving PDF from memory.")

        # At this point, pdf_cache holds the correct PDF bytes.
        response = make_response(pdf_cache)
        
        # --- Set HTTP Headers for SEO and Performance ---
        
        # 1. Content-Type and Disposition
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=blake-rayvid-cv.pdf'
        
        # 2. Cache-Control: Tell browsers/proxies to cache for 1 hour (3600 seconds).
        response.headers['Cache-Control'] = 'public, max-age=3600'
        
        # 3. ETag: A unique identifier for this version of the file.
        #    We generate it by hashing the PDF content.
        etag = hashlib.md5(pdf_cache).hexdigest()
        response.set_etag(etag)
        
        # Let Flask handle the `If-None-Match` request header.
        # If it matches our ETag, Flask will automatically return a 304 Not Modified status.
        return response.make_conditional(request)

    except Exception as e:
        # Provide a helpful error message if something goes wrong.
        return f"An error occurred during PDF generation: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)