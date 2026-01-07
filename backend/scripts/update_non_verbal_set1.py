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

# Credentials (hardcoded for this specific run as per user request context)
ACCESS_KEY = "64805a1a9755e5f7086f9a97880af5ff"
SECRET_KEY = "3d12548740cbdefd1184c9545cbff2e029df2b93f7d22d7aad5bfd9b8939cb7a"
ENDPOINT_URL = "https://jjxusciiuvcjltkreozq.storage.supabase.co/storage/v1/s3"
BUCKET_NAME = "media" # Defaulting to 'media' as per migrate script
REGION = "ap-south-1"

def update_non_verbal_test():
    print("Connecting to Supabase S3...")
    s3 = boto3.client(
        's3',
        endpoint_url=ENDPOINT_URL,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        config=Config(signature_version='s3v4'),
        region_name=REGION
    )

    # 1. Find the Test
    try:
        test = Test.objects.filter(name__icontains="Non-Verbal").filter(name__icontains="Set 1").first()
        if not test:
            print("ERROR: 'Non-Verbal IQ Test - Set 1' not found.")
            return
        
        print(f"Target Test: {test.name} (ID: {test.id})")
        
        # 2. Delete existing questions
        existing_count = Question.objects.filter(test=test).count()
        print(f"Deleting {existing_count} existing questions...")
        Question.objects.filter(test=test).delete()
        
        # 3. Create New Questions
        new_questions_data = [
            {
                "image_file": "uploaded_image_0_1767777507129.png", 
                "answer": "b", 
                "explanation": "The third figure in each row comprises of parts which are not common to the first two figures."
            },
            {
                "image_file": "uploaded_image_1_1767777507129.png",
                "answer": "a",
                "explanation": "There are 3 types of faces, 3 types of bodies, 3 types of hands and 3 types of legs each of which is used only once in a single row. So, the features which have not been used in the first two figures of the third row would combine to produce the missing figure."
            },
            {
                "image_file": "uploaded_image_2_1767777507129.png",
                "answer": "c",
                "explanation": "Each figure in third row comprises of figure marked as 1 of first row in inverted form and figure marked as 2 as it is."
            },
            {
                "image_file": "uploaded_image_3_1767777507129.png",
                "answer": "c",
                "explanation": "As we move from first to the second figure in a row, the figure gets intersected by two mutually perpendicular lines. In the next step, dots appear at the ends of these lines and the lines disappear to give the third figure."
            },
            {
                "image_file": "uploaded_image_4_1767777507129.png",
                "answer": "d",
                "explanation": "The second figure is obtained from the first figure by moving the line segment to the opposite side of the square boundary and replacing it with two similar line segments. Also, the element in the lower-left corner gets replaced by two similar elements - one placed in the upper-left and the other placed in the lower-right corner."
            }
        ]
        
        for i, q_data in enumerate(new_questions_data):
            print(f"Processing Question {i+1}...")
            
            # Create Question
            question = Question.objects.create(
                test=test,
                question_text=f"Identify the missing figure in the pattern (Question {i+1})",
                question_type="mcq",
                difficulty_level="medium",
                correct_answer=q_data["answer"],
                explanation=q_data["explanation"],
                order=i+1,
                options=[
                    {"id": "a", "text": "Figure a"},
                    {"id": "b", "text": "Figure b"},
                    {"id": "c", "text": "Figure c"},
                    {"id": "d", "text": "Figure d"}
                ]
            )
            
            # Upload Image
            # correct path for Docker container since ./backend is mounted to /app
            local_path = Path(f"/app/media/{q_data['image_file']}")
            if not local_path.exists():
                print(f"  Warning: Local image {local_path} not found for Q{i+1}")
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
                
                # Construct Public URL
                # Supabase Storage Public URL Pattern: 
                # https://[PROJECT_ID].supabase.co/storage/v1/object/public/[BUCKET_NAME]/[KEY]
                # Project ID is 'jjxusciiuvcjltkreozq' from endpoint
                project_id = "jjxusciiuvcjltkreozq" 
                public_url = f"https://{project_id}.supabase.co/storage/v1/object/public/{BUCKET_NAME}/{s3_key}"
                
                # Create QuestionImage
                # Store relative path (S3 key) instead of full URL to avoid max_length=100 limit
                # Django's storage backend will reconstruct the full URL
                QuestionImage.objects.create(
                    question=question,
                    image=s3_key, 
                    caption="Question Figure"
                )
                print(f"  ✅ Created Question {i+1} with image path: {s3_key}")
                
            except Exception as e:
                print(f"  ❌ Failed to upload image for Q{i+1}: {e}")

        print("\n✅ Non-Verbal Test Set 1 Updated Successfully.")

    except Exception as e:
        print(f"Update failed: {e}")

if __name__ == "__main__":
    update_non_verbal_test()
