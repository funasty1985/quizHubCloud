from chalice import Chalice
from chalicelib import comprehend_service

app = Chalice(app_name='Capabilities')

comprehend_service = comprehend_service.ComprehendService()

@app.route('/', cors=True)
def index():
    return {'hello': 'world'}

@app.route('/extract-key-phrases', methods=['POST'], cors=True)
def extract_key_phrases():
    request = app.current_request
    body = request.json_body

    text = body.get('text', '')
    if not text:
        return {'error': 'No text provided'}

    key_phrases = comprehend_service.extract_key_phrases(text)
    return {'keyPhrases': key_phrases}
