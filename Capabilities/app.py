import base64
import json

from chalice import Chalice, Response
from chalicelib import comprehend_service
from chalicelib.storage_service import StorageService
from chalicelib.textract_service import TextractService

app = Chalice(app_name='Capabilities')

comprehend_service = comprehend_service.ComprehendService()
storage_service = StorageService('contentcen301323706.aws.ai')
textract_service = TextractService(
    role='arn:aws:iam::975049922009:role/TextractRole',
    )



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
def upload():
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
        paragraph_text_list = textract_service.extract_text(storage_service.get_storage_location(), file_name)

        extracted_text = "\n\n\n".join(paragraph_text_list)

        app.log.debug("Text extraction completed.")
        app.log.debug(f"Extracted text: {extracted_text}")

        return {'filename': file_name, 'extractedText': extracted_text}

    except Exception as e:
        app.log.error(f"Error extracting text from the file: {str(e)}")
        return Response(body={'message': f'Error extracting text from the file: {str(e)}'}, status_code=500)
