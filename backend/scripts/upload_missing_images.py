"""
Upload missing question images to Supabase S3 storage.
Reads image files from a local directory and uploads them to match DB records.

Usage:
    python scripts/upload_missing_images.py --dir /path/to/images

Directory structure expected:
    /path/to/images/
        uploaded_image_0_1767777507129.png
        uploaded_image_1_1767777507129.png
        ...
        non_verbal_q6.png
        non_verbal_q7.png
        ...
        nv3_q1.png
        nv3_q2.png
        ...
"""
import os
import sys
import django
import boto3
from botocore.client import Config
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
django.setup()

from django.conf import settings
from apps.questions.models import QuestionImage
from django.core.files.storage import default_storage


def get_s3_client():
    return boto3.client(
        's3',
        endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        config=Config(signature_version='s3v4'),
        region_name=settings.AWS_S3_REGION_NAME,
    )


def file_matches(filename, stored_path):
    """Check if a filename matches the last segment of a stored path."""
    return filename in stored_path or stored_path.endswith(f'/{filename}')


def upload_missing_images(source_dir):
    source_dir = Path(source_dir)
    if not source_dir.exists():
        print(f"Source directory not found: {source_dir}")
        return

    s3 = get_s3_client()
    bucket = settings.AWS_STORAGE_BUCKET_NAME

    missing = QuestionImage.objects.all()
    total = missing.count()
    uploaded = 0
    skipped = 0

    local_files = list(source_dir.iterdir())
    print(f"Found {len(local_files)} local files in {source_dir}")
    print(f"Checking {total} question images...")

    for qi in missing:
        stored_name = qi.image.name
        s3_key = stored_name

        # Check if already in S3
        try:
            s3.head_object(Bucket=bucket, Key=s3_key)
            skipped += 1
            continue
        except:
            pass

        # Try to find matching local file
        matched = False
        for lf in local_files:
            if lf.name in s3_key or s3_key.endswith(f'/{lf.name}'):
                print(f"  Uploading {lf.name} -> s3://{bucket}/{s3_key}")
                try:
                    s3.upload_file(
                        str(lf),
                        bucket,
                        s3_key,
                        ExtraArgs={'ACL': 'public-read', 'ContentType': 'image/png'}
                    )
                    uploaded += 1
                    matched = True
                except Exception as e:
                    print(f"  FAILED: {e}")
                break

        if not matched:
            print(f"  NOT FOUND: No local file matches '{stored_name}'")

    print(f"\nDone. {uploaded} uploaded, {skipped} already existed, {total - uploaded - skipped} still missing.")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Upload missing question images to S3')
    parser.add_argument('--dir', required=True, help='Directory containing image files')
    args = parser.parse_args()
    upload_missing_images(args.dir)
