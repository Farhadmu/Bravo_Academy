import os
import sys
import django
from pathlib import Path

# Add the project root to the Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
# Database URL should be set via environment variable
# Example: export DATABASE_URL='postgresql://user:password@host:port/database'
django.setup()

from apps.tests.models import Test
from apps.questions.models import Question, QuestionImage
from django.core.files import File

def seed_non_verbal_questions():
    test_id = '9e4d98cd-22c6-436b-8f78-0375e6d5ea99'
    try:
        test = Test.objects.get(id=test_id)
    except Test.DoesNotExist:
        print(f"Test with ID {test_id} not found.")
        return

    # Delete existing questions for this test to avoid duplicates during development
    Question.objects.filter(test=test).delete()

    questions_data = [
        {
            "question_text": "Which of the options below completes the pattern?",
            "question_type": "mcq",
            "options": [
                {"id": "1", "text": "Option 1"},
                {"id": "2", "text": "Option 2"},
                {"id": "3", "text": "Option 3"},
                {"id": "4", "text": "Option 4"},
                {"id": "5", "text": "Option 5"},
                {"id": "6", "text": "Option 6"},
                {"id": "7", "text": "Option 7"},
                {"id": "8", "text": "Option 8"}
            ],
            "correct_answer": "1",
            "order": 1,
            "image_path": "media/questions/images/nv_q1.png"
        },
        {
            "question_text": "Identify the missing piece that completes the sequence.",
            "question_type": "mcq",
            "options": [
                {"id": "1", "text": "Option 1"},
                {"id": "2", "text": "Option 2"},
                {"id": "3", "text": "Option 3"},
                {"id": "4", "text": "Option 4"},
                {"id": "5", "text": "Option 5"},
                {"id": "6", "text": "Option 6"},
                {"id": "7", "text": "Option 7"},
                {"id": "8", "text": "Option 8"}
            ],
            "correct_answer": "3",
            "order": 2,
            "image_path": "media/questions/images/nv_q2.png"
        },
        {
            "question_text": "Which figure is the logical continuation of the series?",
            "question_type": "mcq",
            "options": [
                {"id": "1", "text": "Option 1"},
                {"id": "2", "text": "Option 2"},
                {"id": "3", "text": "Option 3"},
                {"id": "4", "text": "Option 4"},
                {"id": "5", "text": "Option 5"},
                {"id": "6", "text": "Option 6"},
                {"id": "7", "text": "Option 7"},
                {"id": "8", "text": "Option 8"}
            ],
            "correct_answer": "2",
            "order": 3,
            "image_path": "media/questions/images/nv_q3.png"
        },
        {
            "question_text": "Determine the correct domino to fill the empty space.",
            "question_type": "mcq",
            "options": [
                {"id": "1", "text": "Option 1"},
                {"id": "2", "text": "Option 2"},
                {"id": "3", "text": "Option 3"},
                {"id": "4", "text": "Option 4"},
                {"id": "5", "text": "Option 5"},
                {"id": "6", "text": "Option 6"},
                {"id": "7", "text": "Option 7"},
                {"id": "8", "text": "Option 8"}
            ],
            "correct_answer": "4",
            "order": 4,
            "image_path": "media/questions/images/nv_q4.png"
        },
        {
            "question_text": "Which option completes the 3x3 grid pattern?",
            "question_type": "mcq",
            "options": [
                {"id": "1", "text": "Option 1"},
                {"id": "2", "text": "Option 2"},
                {"id": "3", "text": "Option 3"},
                {"id": "4", "text": "Option 4"},
                {"id": "5", "text": "Option 5"},
                {"id": "6", "text": "Option 6"},
                {"id": "7", "text": "Option 7"},
                {"id": "8", "text": "Option 8"}
            ],
            "correct_answer": "2",
            "order": 5,
            "image_path": "media/questions/images/nv_q5.png"
        }
    ]

    for q_data in questions_data:
        question = Question.objects.create(
            test=test,
            question_text=q_data["question_text"],
            question_type=q_data["question_type"],
            options=q_data["options"],
            correct_answer=q_data["correct_answer"],
            order=q_data["order"]
        )
        
        # Add Image
        if os.path.exists(q_data["image_path"]):
            with open(q_data["image_path"], 'rb') as f:
                img_name = os.path.basename(q_data["image_path"])
                QuestionImage.objects.create(
                    question=question,
                    image=File(f, name=img_name),
                    caption="Pattern Question",
                    order=0
                )
            print(f"Created question {q_data['order']} with image.")
        else:
            print(f"Image not found: {q_data['image_path']}")

    # Update test total_questions
    test.total_questions = Question.objects.filter(test=test).count()
    test.save()
    print(f"Test {test.name} updated with {test.total_questions} questions.")

if __name__ == "__main__":
    seed_non_verbal_questions()
