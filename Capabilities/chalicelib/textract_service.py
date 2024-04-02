import boto3
import time

class TextractService:
    def __init__(self):
        self.client = boto3.client('textract')

    def extract_paragraph(self, bucket_name, document_name):
        response = self.client.start_document_text_detection(
            DocumentLocation={
                'S3Object': {
                    'Bucket': bucket_name,
                    'Name': document_name
                }
            }
        )
        job_id = response['JobId']
        print(f"Started job with id: {job_id}")

        status = ""
        while status not in ["SUCCEEDED", "FAILED"]:
            time.sleep(5)
            response = self.client.get_document_text_detection(JobId=job_id)
            status = response['JobStatus']

        if status == "FAILED":
            raise Exception("Textract job failed")

        text_by_page = {}

        next_token = None
        while True:
            kwargs = {'JobId': job_id}
            if next_token:
                kwargs['NextToken'] = next_token
            response = self.client.get_document_text_detection(**kwargs)

            for item in response.get('Blocks', []):
                if item['BlockType'] == "LINE":
                    page_number = item['Page']
                    if page_number not in text_by_page:
                        text_by_page[page_number] = []
                    text_by_page[page_number].append(item['Text'])

            next_token = response.get('NextToken')
            if not next_token:
                break

        pages_text = [{'Page': page, 'Text': " ".join(lines)} for page, lines in text_by_page.items()]
        return pages_text
