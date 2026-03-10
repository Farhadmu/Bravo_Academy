import os
import sys
import django
from django.core.files import File

# Setup Django environment
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, 'apps'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
django.setup()

from apps.tests.models import Test
from apps.questions.models import Question, QuestionImage

def fix_images():
    test_name = "Non-Verbal IQ Test - Set 3"
    test = Test.objects.filter(name=test_name).first()
    if not test:
        print(f"Test '{test_name}' not found!")
        return

    questions = Question.objects.filter(test=test).order_by('order')
    print(f"Found {questions.count()} questions for {test_name}")

    for q in questions:
        image_name = f"nv3_q{q.order}.png"
        image_path = os.path.join(BASE_DIR, 'media/questions/images', image_name)
        
        if os.path.exists(image_path):
            # Check if image already exists to avoid duplicates
            if q.images.exists():
                print(f"Question {q.order} already has an image. Skipping.")
                continue
                
            print(f"Uploading image for Q{q.order}: {image_name}")
            try:
                with open(image_path, 'rb') as f:
                    QuestionImage.objects.create(
                        question=q,
                        image=File(f, name=image_name),
                        caption=f"Visual reasoning for Question {q.order}",
                        order=0
                    )
                print(f"✅ Successfully uploaded and linked image for Q{q.order}")
            except Exception as e:
                print(f"❌ Error uploading image for Q{q.order}: {e}")
        else:
            print(f"⚠️ Image NOT FOUND locally: {image_path}")

    print("\nFix process complete.")

if __name__ == "__main__":
    fix_images()
