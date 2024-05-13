import boto3
import os

class StorageService:
    def __init__(self, storage_location):
        self.client = boto3.client('s3', region_name='us-east-1')
        self.bucket_name = storage_location
        self.resource = boto3.resource('s3', region_name='us-east-1')

    def get_storage_location(self):
        return self.bucket_name

    def download_dir(self, prefix, local, bucket):
        """
            params:
            - prefix: pattern to match in s3
            - local: local path to folder in which to place files
            - bucket: s3 bucket with target contents
            """
        keys = []
        dirs = []
        next_token = ''
        base_kwargs = {
            'Bucket': bucket,
            'Prefix': prefix,
        }
        client = self.client
        while next_token is not None:
            kwargs = base_kwargs.copy()
            if next_token != '':
                kwargs.update({'ContinuationToken': next_token})
            results = client.list_objects_v2(**kwargs)
            contents = results.get('Contents')
            for i in contents:
                k = i.get('Key')
                if k[-1] != '/':
                    keys.append(k)
                else:
                    dirs.append(k)
            next_token = results.get('NextContinuationToken')
        for d in dirs:
            dest_pathname = os.path.join(local, d)
            if not os.path.exists(os.path.dirname(dest_pathname)):
                os.makedirs(os.path.dirname(dest_pathname))
        for k in keys:
            dest_pathname = os.path.join(local, k)
            if not os.path.exists(os.path.dirname(dest_pathname)):
                os.makedirs(os.path.dirname(dest_pathname))
            try:
                client.download_file(bucket, k, dest_pathname)
            except Exception as e:
                print(f"Failed to download {k}: {e}")
    def get_corpus(self):
        local_model_dir = 'chalicelib/nlp/utils/corpus'
        s3_model_dir = 'corpus/s2v_old'
        if not os.path.exists(local_model_dir):
            os.makedirs(local_model_dir)
        else:
            return

        print("###### this function is called #####")
        self.download_dir(s3_model_dir, local_model_dir, self.bucket_name)

    def upload_file(self, file_bytes, file_name):
        self.client.put_object(Bucket=self.bucket_name,
                            Body=file_bytes,
                            Key=file_name,
                            ACL='public-read')

        return {'fileId': file_name,
                'fileUrl': "http://" + self.bucket_name + ".s3.amazonaws.com/" + file_name}
