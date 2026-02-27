import uuid
import boto3
from decouple import config
from fastapi import HTTPException

AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
AWS_REGION = config("AWS_REGION")
AWS_BUCKET_NAME = config("AWS_BUCKET_NAME")

# Create S3 client
s3_client = boto3.client(
    "s3",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

#Generate unique file path inside bucket
def generate_file_name(user_id: int, file_name: str):
    ext = file_name.split(".")[-1]
    unique_file_name = f"{uuid.uuid4()}.{ext}"
    return f"user_{user_id}/{unique_file_name}"


# Generate temporary signed URL (for private bucket)
def generate_presigned_url(file_key: str, expires_in: int = 86400):
    """
    Returns a temporary URL that expires after some time.
    Default expiry = 24 hours (86400 seconds)
    """
    try:
        url = s3_client.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": AWS_BUCKET_NAME,
                "Key": file_key,
            },
            ExpiresIn=expires_in,
        )
        return url

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate image URL: {str(e)}",
        )


# Upload file to S3 (private bucket)
def upload_file_to_s3(file, user_id: int):
    file_key = generate_file_name(user_id, file.filename)

    try:
        s3_client.upload_fileobj(
            file.file,
            AWS_BUCKET_NAME,
            file_key,
            ExtraArgs={"ContentType": file.content_type},
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"File upload failed: {str(e)}",
        )

    #IMPORTANT: return file_key (NOT URL anymore)
    return file_key