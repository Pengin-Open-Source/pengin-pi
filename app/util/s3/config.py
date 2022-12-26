import os

import boto3
# from app.util.log import log
from dotenv import load_dotenv

load_dotenv()


class File:
    def __init__(self):
        self.aws_access_key_id = os.getenv('S3_KEY')
        self.aws_secret_access_key = os.getenv('S3_SECRET')
        self.aws_bucket = os.getenv('S3_BUCKET')
        self.aws_location = os.getenv('S3_LOCATION')

        self.conn = boto3.client("s3",
                                 aws_access_key_id=self.aws_access_key_id,
                                 aws_secret_access_key=self.aws_secret_access_key)

    def upload(self, file):
        """
        param file: Readable-binary file-like object
        """
        try:
            self.conn.upload_fileobj(
                file, self.aws_bucket, os.path.basename(file.name))
        except Exception as e:
            print('Exception: ' + str(e))
            return e

    def download(self, file_name):
        try:
            with open(file_name, 'wb') as file:
                self.conn.download_fileobj(self.aws_bucket, file_name, file)
        except Exception as e:
            print('Exception: ' + str(e))
            return e

    def get_URL(self, file_name, exp=900):
        return self.conn.generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': self.aws_bucket, 'Key': file_name},
            ExpiresIn=exp)


if __name__ == "__main__":
    file = File()