import os
import sys
import django
import boto3
from botocore.client import Config
from pathlib import Path

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from apps.tests.models import Test
from apps.questions.models import Question, QuestionImage

# Credentials
ACCESS_KEY = "64805a1a9755e5f7086f9a97880af5ff"
SECRET_KEY = "3d12548740cbdefd1184c9545cbff2e029df2b93f7d22d7aad5bfd9b8939cb7a"
ENDPOINT_URL = "https://jjxusciiuvcjltkreozq.storage.supabase.co/storage/v1/s3"
BUCKET_NAME = "media"
REGION = "ap-south-1"

def update_non_verbal_set2_part1():
    print("Connecting to Supabase S3...")
    s3 = boto3.client(
        's3',
        endpoint_url=ENDPOINT_URL,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        config=Config(signature_version='s3v4'),
        region_name=REGION
    )

    try:
        # Check or Create Set 2
        test_name = "Non-Verbal IQ Test - Set 2"
        test = Test.objects.filter(name=test_name).first()
        
        if not test:
            print(f"Creating new test: {test_name}")
            test = Test.objects.create(
                name=test_name,
                description="Determine your Non-Verbal IQ Level. (Set 2)",
                category="non-verbal",
                duration_minutes=9,
                total_questions=0, # Will update automatically or we can set strict
                price=0.00,
                passing_score=50
            )
            print(f"✅ Created Test: {test.name} (ID: {test.id})")
        else:
            print(f"Found existing Test: {test.name} (ID: {test.id})")
            if test.duration_minutes != 9:
                test.duration_minutes = 9
                test.save()
                print("✅ Updated duration to 9 minutes.")

        # New Questions 1-5
        new_questions_data = [
            {
                "image_file": "uploaded_image_0_1767785417022.png", 
                "answer": "c", 
                "explanation": "The central part of the first figure rotates either 90 degrees clockwise or 90 degrees anti-clockwise to form the central part of the second figure. The central part of the first figure rotates 180 degrees to form the central part of the third figure."
            },
            {
                "image_file": "uploaded_image_1_1767785417022.png",
                "answer": "b",
                "explanation": "In each row, the third figure is obtained when, in the second figure, the first figure is placed inside it, and in the first figure again, the second figure is placed inside it, reducing its size."
            },
            {
                "image_file": "uploaded_image_2_1767785417022.png",
                "answer": "c",
                "explanation": "As we move from left to right in each row, the figure rotates through an angle of 135 degrees anti-clockwise at each step."
            },
            {
                "image_file": "uploaded_image_3_1767785417022.png",
                "answer": "b",
                "explanation": "In each column, three figures with one circle and one square each are present in such a way that three different patterns of both the circle and the square are present in all columns."
            },
            {
                "image_file": "uploaded_image_4_1767785417022.png",
                "answer": "a",
                "explanation": "The second figure in each row is obtained by joining the lower part of the first figure with its upper part."
            }
        ]
        
        start_order = 1
        
        for i, q_data in enumerate(new_questions_data):
            current_order = start_order + i
            print(f"Processing Question {current_order}...")
            
            # Check if exists to avoid duplication
            if Question.objects.filter(test=test, order=current_order).exists():
                print(f"  Warning: Question {current_order} already exists. Skipping creation (but might check image).")
                continue

            # Create Question
            question = Question.objects.create(
                test=test,
                question_text=f"Identify the missing figure in the pattern (Question {current_order})",
                question_type="mcq",
                difficulty_level="medium",
                correct_answer=q_data["answer"],
                explanation=q_data["explanation"],
                order=current_order,
                options=[
                    {"id": "a", "text": "Figure a"},
                    {"id": "b", "text": "Figure b"},
                    {"id": "c", "text": "Figure c"},
                    {"id": "d", "text": "Figure d"}
                ]
            )
            
            # Upload Image
            local_path = Path(f"/app/media/{q_data['image_file']}")
            if not local_path.exists():
                local_path = Path(f"/var/www/online-edu/backend/media/{q_data['image_file']}")
            
            if not local_path.exists():
                print(f"  Warning: Local image {local_path} not found for Q{current_order}")
                continue
                
            s3_key = f"questions/{test.id}/{q_data['image_file']}"
            try:
                print(f"  Uploading {q_data['image_file']} to s3://{BUCKET_NAME}/{s3_key}...")
                with open(local_path, "rb") as f:
                    s3.upload_fileobj(
                        f,
                        BUCKET_NAME,
                        s3_key,
                        ExtraArgs={'ACL': 'public-read', 'ContentType': 'image/png'}
                    )
                
                QuestionImage.objects.create(
                    question=question,
                    image=s3_key, 
                    caption="Question Figure"
                )
                print(f"  ✅ Created Question {current_order} with image path: {s3_key}")
                
            except Exception as e:
                print(f"  ❌ Failed to upload image for Q{current_order}: {e}")

        print("\n✅ Non-Verbal Test Set 2 Updated (Questions 1-5 Added).")

    except Exception as e:
        print(f"Update failed: {e}")

if __name__ == "__main__":
    update_non_verbal_set2_part1()
