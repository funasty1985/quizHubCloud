from chalice import Chalice, Response
import json
import base64
from chalicelib.storage_service import StorageService
from chalicelib.textract_service import TextractService
from chalicelib.db_service import DbService
import time
from chalicelib.nlp.utils.Pipeline import GenQuestionPipeline
from datetime import datetime
from bson.objectid import ObjectId

app = Chalice(app_name='Capabilities')
app.debug = True

storage_service = StorageService('contentcen301323706.aws.ai')
textract_service = TextractService()
db_service = DbService("mongodb+srv://portfolioApp:Fu2017fu@cluster0.ykgbhqe.mongodb.net/project1?retryWrites=true&w=majority")
nlp_service = GenQuestionPipeline()

@app.route('/upload', methods=['POST'], cors=True)
def upload_pdf():
    try:
        request_data = json.loads(app.current_request.raw_body)
        file_name = request_data['filename']
        file_bytes = base64.b64decode(request_data['filebytes'])

        app.log.debug(f"Attempting to upload {file_name} to S3.")
        file_info = storage_service.upload_file(file_bytes, file_name)
        app.log.debug(f"Upload successful: {file_info}")

        return file_info
    except Exception as e:
        app.log.error(f"Error processing or uploading file: {str(e)}")
        return Response(body={'message': f'Error processing or uploading file: {str(e)}'}, status_code=500)

@app.route('/extract-paragraph', methods=['POST'], cors=True)
def extract_paragraph():
    try:
        start_time_1 = time.time()
        request_data = json.loads(app.current_request.raw_body.decode('utf-8'))
        file_name = request_data['filename']

        # extract text
        app.log.debug("Text extraction started.")
        extracted_text = textract_service.extract_paragraph(storage_service.get_storage_location(), file_name)
        text_by_page = [o['Text'] for o in extracted_text]
        app.log.debug("Text extraction completed.")
        duration = time.time() - start_time_1
        app.log.debug(f"Paragraph extraction completed in {duration:.2f} seconds.")

        # generate question
        app.log.debug("Generate Questions started.")
        start_time = time.time()
        questions = nlp_service.pipeline(text_by_page)
        app.log.debug("Generate Questions completed.")
        duration = time.time() - start_time
        app.log.debug(f"Generate Questions completed in {duration:.2f} seconds.")

        # persist question
        app.log.debug("Upload Questions Started")
        start_time = time.time()
        date_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        # create quiz in db
        quiz_id = db_service.create_quiz(
            user=db_service.user,
            title=f"quiz created at {date_time}",
            description="This is a wonderful test"
        )
        # persist questions
        db_service.upload_questions_by_quiz_id(questions, quiz_id)
        duration = time.time() - start_time
        app.log.debug(f"Upload Questions ended in {duration:.2f} seconds.")

        duration = time.time() - start_time_1
        app.log.debug(f"TOTAL PROCESS TAKES {duration:.2f} seconds.")
        return {'filename': file_name, 'questions': questions}

    except Exception as e:
        app.log.error(f"Error extracting text from the file: {str(e)}")
        return Response(body={'message': f'Error extracting text from the file: {str(e)}'}, status_code=500)

