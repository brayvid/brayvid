# generate_pdf.py
import os
from flask import Flask, render_template
from weasyprint import HTML, CSS

# Create a minimal Flask app instance just for rendering the template
app = Flask(__name__)

# Ensure the root_path is correctly set for the template loader
# (usually handles itself if script is at root, but explicit is safer)
app.root_path = os.path.dirname(os.path.abspath(__file__))

print("Starting PDF generation during Docker build...")

try:
    with app.app_context():
        with app.test_request_context():
            # Render the HTML template, passing a flag to hide the download button.
            html_string = render_template('index.html', is_pdf_render=True)

    # base_url is crucial for WeasyPrint to find static files like your fonts.
    # It must be an absolute path within the container.
    base_url = os.path.join(app.root_path, 'static')

    # Define the PDF page layout.
    page_layout_css = CSS(string="@page { size: letter; margin: 0.02in; }")
    
    html_obj = HTML(string=html_string, base_url=base_url)
    pdf_bytes = html_obj.write_pdf(stylesheets=[page_layout_css])

    # Save the generated PDF to a file within the Docker image
    pdf_output_path = os.path.join(app.root_path, 'blake-rayvid-cv.pdf')
    with open(pdf_output_path, 'wb') as f:
        f.write(pdf_bytes)

    print(f"PDF generated successfully and saved to {pdf_output_path}")

except Exception as e:
    print(f"Error during PDF generation in Docker build: {e}")
    # Re-raise the exception to make the Docker build fail explicitly
    raise