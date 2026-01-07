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

def update_non_verbal_test_part4():
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
        test = Test.objects.filter(name__icontains="Non-Verbal").filter(name__icontains="Set 1").first()
        if not test:
            print("ERROR: 'Non-Verbal IQ Test - Set 1' not found.")
            return
        
        print(f"Target Test: {test.name} (ID: {test.id})")
        
        # New Questions 16-20
        new_questions_data = [
            {
                "image_file": "uploaded_image_0_1767779715197.png", 
                "answer": "d", 
                "explanation": "In each row, the second figure is obtained by shading one of the four parts of the first figure, and the third figure is obtained by shading two out of the four parts of the first figure."
            },
            {
                "image_file": "uploaded_image_1_1767779715197.png",
                "answer": "a",
                "explanation": "There are three types of triangular shadings, three types of legs, and three positions of circles. Each type is used only once in a row. Also, in each row, two circles are shaded."
            },
            {
                "image_file": "uploaded_image_2_1767779715197.png",
                "answer": "b",
                "explanation": "In each row, the number of elements in the third figure is equal to the difference in the number of elements in the first and second figures. Also, the third figure has the same types of elements (if any) as the elements in the first figure."
            },
            {
                "image_file": "uploaded_image_3_1767779715197.png",
                "answer": "a",
                "explanation": "The shapes follow a specific sequence: the triangle follows the circle, and the square follows the triangle."
            },
            {
                "image_file": "uploaded_image_4_1767779715197.png",
                "answer": "c",
                "explanation": "In each row, there are two, three, and four similar squares present."
            }
        ]
        
        start_order = 16
        
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
            # Using /app/media for Docker env 
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

        print("\n✅ Non-Verbal Test Set 1 Updated (Questions 16-20 Added).")

    except Exception as e:
        print(f"Update failed: {e}")

if __name__ == "__main__":
    update_non_verbal_test_part4()
