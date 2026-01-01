
import os
import django
import sys
import shutil

# Setup Django environment
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, 'apps'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
django.setup()

from apps.tests.models import Test
from apps.questions.models import Question, QuestionImage
from apps.users.models import User
from django.core.files import File

def seed_data():
    print("Seeding Non-Verbal IQ Test - Set 1...")

    # 1. Get admin user
    admin_user = User.objects.filter(is_superuser=True).first()
    if not admin_user:
        print("Admin user not found, creating...")
        admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')

    # 2. Create the Test
    test_name = "Non-Verbal IQ Test - Set 1"
    test, created = Test.objects.get_or_create(
        name=test_name,
        defaults={
            "description": "Visual pattern recognition and spatial reasoning test. Observe the patterns and select the correct missing piece.",
            "duration_minutes": 20,
            "price": 0.00,
            "is_active": True,
            "created_by": admin_user,
            "total_questions": 5 # Will update automatically
        }
    )
    
    if created:
        print(f"Created new test: {test_name}")
    else:
        print(f"Updating existing test: {test_name}")

    # 3. Define Questions
    # Since visual questions are all about "Select the correct option", we can use a generic text.
    generic_text = "Which of the options below completes the pattern?"
    
    # 8 Generic Options
    options = [{"id": str(i), "text": f"Option {i}"} for i in range(1, 9)]

    questions_data = [
        {"file": "q1.png", "answer": "1"}, # Placeholder answer
        {"file": "q2.png", "answer": "1"},
        {"file": "q3.png", "answer": "1"},
        {"file": "q4.png", "answer": "1"},
        {"file": "q5.png", "answer": "1"},
    ]

    # Source directory for images
    source_dir = os.path.join(BASE_DIR, 'media', 'questions', 'images', 'non-verbal', 'set1')

    # clear existing questions to avoid duplicates
    Question.objects.filter(test=test).delete()

    for idx, q_data in enumerate(questions_data, 1):
        # Create Question
        question = Question.objects.create(
            test=test,
            question_text=generic_text,
            question_type='mcq',
            options=options,
            correct_answer=q_data['answer'],
            difficulty_level='medium',
            order=idx,
            bank_order=1000 + idx, # Start non-verbal bank ID from 1000
            explanation="Visual recognition required."
        )

        # Handle Image
        filename = q_data['file']
        source_path = os.path.join(source_dir, filename)
        
        if os.path.exists(source_path):
            with open(source_path, 'rb') as img_file:
                # We create the QuestionImage object
                q_image = QuestionImage(
                    question=question,
                    caption="Pattern Question",
                    order=1
                )
                # save() handles the file copy to the upload_to location
                q_image.image.save(filename, File(img_file), save=True)
                print(f"Created Q{idx} with image {filename}")
        else:
            print(f"WARNING: Image not found for Q{idx}: {source_path}")

    print("Non-Verbal Set 1 seeding complete!")

if __name__ == '__main__':
    seed_data()
