import boto3
import os

s3 = boto3.client(
   "s3",
   aws_access_key_id=os.getenv('S3_KEY'),
   aws_secret_access_key=os.getenv('S3_SECRET')
)


def upload_file_to_s3(file, bucket_name, acl="public-read"):
    try:
        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": acl
            }
        )
    except Exception as e:
        print('Exception:' + e)
        return e
    return "{}{}".format(os.getenv("S3_LOCATION"), file.filename)
