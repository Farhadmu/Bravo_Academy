import os
import boto3
from botocore.client import Config
from pathlib import Path

# Credentials
ACCESS_KEY = "64805a1a9755e5f7086f9a97880af5ff"
SECRET_KEY = "3d12548740cbdefd1184c9545cbff2e029df2b93f7d22d7aad5bfd9b8939cb7a"
ENDPOINT_URL = "https://jjxusciiuvcjltkreozq.storage.supabase.co/storage/v1/s3"
BUCKET_NAME = "media"
REGION = "ap-south-1"

def migrate_media():
    print(f"Connecting to Supabase S3 at {ENDPOINT_URL}...")
    s3 = boto3.resource(
        's3',
        endpoint_url=ENDPOINT_URL,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        config=Config(signature_version='s3v4'),
        region_name=REGION
    )

    try:
        # Check if bucket exists
        bucket = s3.Bucket(BUCKET_NAME)
        if bucket.creation_date:
            print(f"Bucket '{BUCKET_NAME}' already exists.")
        else:
            print(f"Bucket '{BUCKET_NAME}' does not exist. Attempting to create it...")
            s3.create_bucket(Bucket=BUCKET_NAME, CreateBucketConfiguration={'LocationConstraint': REGION})
            print(f"Bucket '{BUCKET_NAME}' created successfully.")
    except Exception as e:
        print(f"Error checking/creating bucket: {e}")
        print("Please ensure you have created a PUBLIC bucket named 'media' in the Supabase Dashboard.")
        # If we can't create it, we'll still try to upload if it might exist but we just can't list it
    
    # Local media directory
    media_root = Path("/var/www/online-edu/backend/media")
    if not media_root.exists():
        print(f"Local media root {media_root} does not exist. Nothing to migrate.")
        return

    print("Scanning for local media files...")
    for file_path in media_root.rglob("*"):
        if file_path.is_file():
            # Calculate S3 key (relative to media root)
            relative_path = file_path.relative_to(media_root)
            s3_key = str(relative_path).replace("\\", "/") # Ensure forward slashes for S3
            
            print(f"Uploading {file_path} to s3://{BUCKET_NAME}/{s3_key}...")
            try:
                s3.meta.client.upload_file(
                    str(file_path),
                    BUCKET_NAME,
                    s3_key,
                    ExtraArgs={'ACL': 'public-read'} # Make sure it's public
                )
                print(f"Successfully uploaded {s3_key}")
            except Exception as e:
                print(f"Failed to upload {s3_key}: {e}")

if __name__ == "__main__":
    migrate_media()
