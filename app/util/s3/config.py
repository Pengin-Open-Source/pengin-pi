import boto3
import os
#from app.util.log import log


class File:
    def __init__(self):
        self.aws_access_key_id = os.getenv('S3_KEY')
        self.aws_secret_access_key = os.getenv('S3_SECRET')
        self.aws_bucket = os.getenv('S3_BUCKET')
        self.aws_location = os.getenv('S3_LOCATION')
        self.conn = boto3.client("s3",
                                       aws_access_key_id=self.aws_access_key_id,
                                       aws_secret_access_key=self.aws_secret_access_key )

    def create(self, file):
        try:
            self.conn.upload_fileobj(file, self.aws_bucket, file.filename)
        except Exception as e:
            print('Exception:' + str(e))
            return e
    
    def read(self, file):
        try:
            with open(file, 'wb') as f:
                result = self.conn.download_fileobj(self.aws_bucket, file.filename, f)
                return result
                
        except Exception as e:
            print('Exception:' + str(e))
            return e
