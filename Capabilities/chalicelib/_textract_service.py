import boto3
import json
import sys
import time

class TextractService:
    jobId = ''
    region_name = ''

    roleArn = ''
    bucket = ''
    document = ''

    sqsQueueUrl = ''
    snsTopicArn = ''
    processType = ''

    current_page = 1
    page_text_list = []
    def __init__(self, role, region=None):
        self.roleArn = role
        self.region_name = region

        self.textract = boto3.client('textract', region_name=self.region_name)
        self.sqs = boto3.client('sqs', region_name=self.region_name)
        self.sns = boto3.client('sns', region_name=self.region_name)

    def extract_text(self, bucket_name, document_name):

        self.CreateTopicandQueue()
        self.ProcessDocument(document=document_name, bucket_name=bucket_name)
        self.DeleteTopicandQueue()

        return self.page_text_list
    def ProcessDocument(self, bucket_name, document):
        jobFound = False

        # Determine which type of processing to perform
        response = self.textract.start_document_text_detection(
            DocumentLocation={'S3Object': {'Bucket': bucket_name, 'Name': document}},
            NotificationChannel={'RoleArn': self.roleArn, 'SNSTopicArn': self.snsTopicArn})
        print('Processing type: Detection')

        print('Start Job Id: ' + response['JobId'])
        dotLine = 0
        while jobFound == False:
            sqsResponse = self.sqs.receive_message(QueueUrl=self.sqsQueueUrl, MessageAttributeNames=['ALL'],
                                                   MaxNumberOfMessages=10)

            if sqsResponse:
                if 'Messages' not in sqsResponse:
                    if dotLine < 40:
                        print('.', end='')
                        dotLine = dotLine + 1
                    else:
                        print()
                        dotLine = 0
                    sys.stdout.flush()
                    time.sleep(5)
                    continue

                for message in sqsResponse['Messages']:
                    notification = json.loads(message['Body'])
                    textMessage = json.loads(notification['Message'])
                    print(textMessage['JobId'])
                    print(textMessage['Status'])
                    if str(textMessage['JobId']) == response['JobId']:
                        print('Matching Job Found:' + textMessage['JobId'])
                        jobFound = True
                        self.GetResults(textMessage['JobId'])
                        self.sqs.delete_message(QueueUrl=self.sqsQueueUrl,
                                                ReceiptHandle=message['ReceiptHandle'])
                    else:
                        print("Job didn't match:" +
                              str(textMessage['JobId']) + ' : ' + str(response['JobId']))
                    # Delete the unknown message. Consider sending to dead letter queue
                    self.sqs.delete_message(QueueUrl=self.sqsQueueUrl,
                                            ReceiptHandle=message['ReceiptHandle'])

        print('Done!')

    def CreateTopicandQueue(self):
        millis = str(int(round(time.time() * 1000)))

        # Create SNS topic
        snsTopicName = "AmazonTextractTopic" + millis

        topicResponse = self.sns.create_topic(Name=snsTopicName)
        self.snsTopicArn = topicResponse['TopicArn']

        # create SQS queue
        sqsQueueName = "AmazonTextractQueue" + millis
        self.sqs.create_queue(QueueName=sqsQueueName)
        self.sqsQueueUrl = self.sqs.get_queue_url(QueueName=sqsQueueName)['QueueUrl']

        attribs = self.sqs.get_queue_attributes(QueueUrl=self.sqsQueueUrl,
                                                AttributeNames=['QueueArn'])['Attributes']

        sqsQueueArn = attribs['QueueArn']

        # Subscribe SQS queue to SNS topic
        self.sns.subscribe(
            TopicArn=self.snsTopicArn,
            Protocol='sqs',
            Endpoint=sqsQueueArn)

        # Authorize SNS to write SQS queue
        policy = """{{
          "Version":"2012-10-17",
          "Statement":[
            {{
              "Sid":"MyPolicy",
              "Effect":"Allow",
              "Principal" : {{"AWS" : "*"}},
              "Action":"SQS:SendMessage",
              "Resource": "{}",
              "Condition":{{
                "ArnEquals":{{
                  "aws:SourceArn": "{}"
                }}
              }}
            }}
          ]
        }}""".format(sqsQueueArn, self.snsTopicArn)

        self.sqs.set_queue_attributes(
            QueueUrl=self.sqsQueueUrl,
            Attributes={
                'Policy': policy
            })

    def DeleteTopicandQueue(self):
        self.sqs.delete_queue(QueueUrl=self.sqsQueueUrl)
        self.sns.delete_topic(TopicArn=self.snsTopicArn)

    # Display information about a block
    def DisplayBlockInfo(self, block):

        if 'Text' in block and block['BlockType'] == 'LINE':
            print("Type: " + block['BlockType'])
            print("Text: " + block['Text'])
            print(block['Page'])

    def GetResults(self, jobId):
        maxResults = 1000
        paginationToken = None
        finished = False

        paragraph_text = ''
        while finished == False:

            response = None
            if paginationToken == None:
                response = self.textract.get_document_text_detection(JobId=jobId,
                                                                     MaxResults=maxResults)
            else:
                response = self.textract.get_document_text_detection(JobId=jobId,
                                                                     MaxResults=maxResults,
                                                                     NextToken=paginationToken)

            blocks = response['Blocks']
            print('Detected Document Text')
            print('Pages: {}'.format(response['DocumentMetadata']['Pages']))

            # Display block information
            for block in blocks:
                if block['Page'] == self.current_page:

                    if block['BlockType'] == 'LINE':
                        paragraph_text += block['Text'] + ' '
                else:
                    self.current_page = block['Page']
                    self.page_text_list.append(paragraph_text)
                    paragraph_text = ''
                    print()
                self.DisplayBlockInfo(block)

            if 'NextToken' in response:
                paginationToken = response['NextToken']
            else:
                finished = True

        # insert the last page
        self.page_text_list.append(paragraph_text)


