# app.py
import os
import hashlib
from flask import Flask, render_template, make_response, send_from_directory, request

app = Flask(__name__)

@app.route('/')
def resume():
    """Renders the HTML resume page."""
    return render_template('index.html')

@app.route('/download-pdf')
def download_pdf():
    """Serves the pre-generated PDF file."""
    return send_from_directory(
        app.root_path,
        'blake-rayvid-cv.pdf',
        mimetype='application/pdf',
        as_attachment=True,
        download_name='blake-rayvid-cv.pdf',
        last_modified=os.path.getmtime(os.path.join(app.root_path, 'blake-rayvid-cv.pdf'))
    )

@app.route('/health')
def health_check():
    """
    A simple healthcheck endpoint that returns a 200 OK.
    This is used by the platform to confirm the container is live.
    """
    return {"status": "ok"}, 200

if __name__ == '__main__':
    app.run(debug=True)