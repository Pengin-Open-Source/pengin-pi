import os

import boto3
# from app.util.log import log
from dotenv import load_dotenv
from app.util.uuid import id


load_dotenv()


class File:
    def __init__(self, aws_access_key_id=os.getenv('S3_KEY'),
                 aws_secret_access_key=os.getenv('S3_SECRET'),
                 aws_bucket=os.getenv('S3_BUCKET'),
                 aws_location=os.getenv('S3_LOCATION')):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.aws_bucket = aws_bucket
        self.aws_location = aws_location        
        self.conn = boto3.client("s3",
                                 aws_access_key_id=self.aws_access_key_id,
                                 aws_secret_access_key=self.aws_secret_access_key)

    def create(self, file):
        """
        param file: Readable-binary file-like object
        """
        try:
            ext = file.filename.split('.')[-1] #get the file extension
            filename = id() + '.' + ext
            self.conn.upload_fileobj(file, self.aws_bucket, filename)
            return filename
        except Exception as e:
            print('Exception: ' + str(e))
            return "/static/images/test.png"

    def read(self, file_name):
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
    #file = File("AWS ID", "AWS KEY", "AWS BUCKET", "AWS LOCATION")
    pass
