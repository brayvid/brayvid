# app.py
import os
from flask import Flask, render_template, send_from_directory, redirect, url_for

app = Flask(__name__)

# Handle 404 errors by redirecting to the homepage
@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('resume'))

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'src/favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def resume():
    """Renders the HTML resume page."""
    return render_template('index.html')

@app.route('/download-pdf')
def download_pdf():
    """Serves the pre-generated PDF file from the Docker image."""
    try:
        return send_from_directory(
            directory=app.root_path,
            path='blake-rayvid-cv.pdf',
            mimetype='application/pdf',
            as_attachment=True,
            download_name='blake-rayvid-cv.pdf'
        )
    except FileNotFoundError:
        return "Error: The PDF file was not found. The build process may have failed.", 500

@app.route('/health')
def health_check():
    """A simple healthcheck endpoint."""
    return {"status": "ok"}, 200

if __name__ == '__main__':
    # For local testing, run `python generate_pdf.py` first
    # to create the PDF file before running this server.
    app.run(debug=True)