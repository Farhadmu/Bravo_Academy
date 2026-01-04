import sys
import os
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

import django
import boto3
from django.conf import settings

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
django.setup()

from apps.questions.models import QuestionImage

def cleanup_media():
    print("Connecting to Supabase S3 for cleanup...")
    
    # Get credentials from settings
    access_key = settings.AWS_ACCESS_KEY_ID
    secret_key = settings.AWS_SECRET_ACCESS_KEY
    endpoint_url = settings.AWS_S3_ENDPOINT_URL
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    region = settings.AWS_S3_REGION_NAME

    if not all([access_key, secret_key, endpoint_url, bucket_name]):
        print("Missing S3 configuration in settings. Cannot proceed.")
        return

    s3 = boto3.client(
        's3',
        endpoint_url=endpoint_url,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region
    )

    print("Fetching used images from database...")
    used_images = set()
    for img in QuestionImage.objects.all():
        if img.image:
            used_images.add(img.image.name)
    
    print(f"Found {len(used_images)} images in use by the database.")
    for img_name in sorted(used_images):
        print(f"  - {img_name}")

    print("\nScanning Supabase bucket for all files...")
    all_files = []
    paginator = s3.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=bucket_name):
        if 'Contents' in page:
            for obj in page['Contents']:
                all_files.append(obj['Key'])

    print(f"Found {len(all_files)} total files in bucket.")

    to_delete = []
    for file_key in all_files:
        # Check if the file is used
        # Note: Django storage usually stores the relative path, so check both
        if file_key not in used_images:
            to_delete.append(file_key)

    if not to_delete:
        print("No orphan files found. Everything is clean!")
        return

    print(f"\nFound {len(to_delete)} orphan files to delete:")
    for file_key in to_delete:
        print(f"  - {file_key}")

    print("\nDeleting files...")
    for file_key in to_delete:
        try:
            s3.delete_object(Bucket=bucket_name, Key=file_key)
            print(f"Successfully deleted: {file_key}")
        except Exception as e:
            print(f"Failed to delete {file_key}: {e}")
    print("\nCleanup complete!")

if __name__ == "__main__":
    cleanup_media()
