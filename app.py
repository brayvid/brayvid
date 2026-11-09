# app.py
from datetime import datetime
import os
from dotenv import load_dotenv
from flask import (
    Flask,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
import requests

load_dotenv()

app = Flask(__name__)

DISCORD_WEBHOOK_URL = os.environ.get('DISCORD_WEBHOOK_URL')

# Handle 404 errors by redirecting to the homepage
@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('resume'))

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'src/favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/robots.txt')
def robots_txt():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'robots.txt', mimetype='text/plain')

@app.route('/llms.txt')
def llms_txt():
    """Serves the llms.txt Markdown CV to AI agents."""
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'llms.txt', 
        mimetype='text/markdown'
    )

@app.route('/')
def resume():
    """Renders the HTML resume page."""
    return render_template('index.html')

@app.route('/download-pdf')
def download_pdf():
    """Serves the pre-generated PDF file from the Docker image."""
    if DISCORD_WEBHOOK_URL:
        try:
            user_agent = request.headers.get('User-Agent', 'Unknown Device')
            referrer = request.referrer or 'Direct / None'
            payload = {
                'embeds': [{
                    'title': '🚨 CV Downloaded!',
                    'color': 16766720,
                    'fields': [
                        {'name': 'Site', 'value': 'cv.blakerayvid.com', 'inline': True},
                        {'name': 'Referrer', 'value': referrer, 'inline': True},
                        {'name': 'Device / Browser', 'value': user_agent[:100] + '...' if len(user_agent) > 100 else user_agent, 'inline': False}
                    ],
                    'footer': {'text': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC') + ' | Railway'}
                }]
            }
            requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=2)
        except Exception as e:
            app.logger.error(f'Discord notification failed: {e}')

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