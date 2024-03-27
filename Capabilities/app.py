from chalice import Chalice
from chalicelib import comprehend_service
from chalicelib.storage_service import StorageService
from chalicelib.textract_service import TextractService

app = Chalice(app_name='Capabilities')

comprehend_service = comprehend_service.ComprehendService()
storage_service = StorageService('contentcen301236221.aws.ai')
textract_service = TextractService()

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

@app.route('/upload', methods=['POST'], cors=True)
def upload_pdf():
    try:
        request_data = json.loads(app.current_request.raw_body)
        file_name = request_data['filename']
        file_bytes = base64.b64decode(request_data['filebytes'])

        app.log.debug(f"Attempting to upload {file_name} to S3.")
        pdf_info = storage_service.upload_file(file_bytes, file_name)
        app.log.debug(f"Upload successful: {pdf_info}")

        return pdf_info
    except Exception as e:
        app.log.error(f"Error processing or uploading PDF file: {str(e)}")
        return Response(body={'message': f'Error processing or uploading PDF file: {str(e)}'}, status_code=500)


@app.route('/extract-text', methods=['POST'], cors=True)
def extract_text():
    try:
        request_data = json.loads(app.current_request.raw_body)
        file_name = request_data['filename']

        app.log.debug(f"Starting text extraction for {file_name}.")
        extracted_text = textract_service.extract_text(storage_service.get_storage_location(), file_name)

        app.log.debug("Text extraction completed.")
        app.log.debug(f"Extracted text: {extracted_text}")

        return {'filename': file_name, 'extractedText': extracted_text}

    except Exception as e:
        app.log.error(f"Error extracting text from PDF: {str(e)}")
        return Response(body={'message': f'Error extracting text from PDF: {str(e)}'}, status_code=500)
