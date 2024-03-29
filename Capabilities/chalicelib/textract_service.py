import boto3
import time


class TextractService:
    def __init__(self):
        self.client = boto3.client('textract')

    def extract_text(self, bucket_name, document_name):

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

        text = ""
        if status == "SUCCEEDED":
            for item in response['Blocks']:
                if item['BlockType'] == "LINE":
                    text += item['Text'] + "\n"
        return text

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

        """
        different file types have different thresholds for paragraph detection
        """
        file_extension = '.' + document_name.split('.')[-1].lower()
        if file_extension == '.pdf':
            threshold = 0.02
        else:
            threshold = 0.05

        paragraphs = []
        current_paragraph = ""
        last_top = None
        for item in response.get('Blocks', []):
            if item['BlockType'] == "LINE":
                current_top = item['Geometry']['BoundingBox']['Top']
                if last_top is not None and (current_top - last_top) > threshold:
                    paragraphs.append(current_paragraph.strip())
                    current_paragraph = item['Text'] + " "
                else:
                    current_paragraph += item['Text'] + " "
                last_top = current_top

        if current_paragraph:
            paragraphs.append(current_paragraph.strip())

        return paragraphs
