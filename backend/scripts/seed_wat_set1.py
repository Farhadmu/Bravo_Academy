
import os
import sys
import django

# Add project root and backend directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir) # /var/www/online-edu/backend
project_root = os.path.dirname(backend_dir) # /var/www/online-edu
sys.path.append(project_root)
sys.path.append(backend_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.config.settings.development')
django.setup()

from apps.questions.models import Question
from apps.tests.models import Test
from django.contrib.auth import get_user_model

User = get_user_model()

def seed_wat_set1():
    print("Seeding WAT Set 1...")
    
    # 1. Create or Get the Test
    admin_user = User.objects.filter(is_superuser=True).first()
    if not admin_user:
        print("Error: No admin user found. Please create one.")
        return

    test_name = "WAT Set 1"
    test, created = Test.objects.get_or_create(
        name=test_name,
        category='verbal' if 'Non-Verbal' not in locals().get('test_name', '') and 'WAT' not in locals().get('test_name', '') else ('non-verbal' if 'Non-Verbal' in locals().get('test_name', '') else 'wat'),
        defaults={
            'description': "Word Association Test Set 1. You will see 80 words, one by one, for 10 seconds each. Write a sentence for each word on your answer sheet.",
            'duration_minutes': 14, # 80 words * 10s = 800s approx 13.3 mins, set 14 for buffer
            'total_questions': 80,
            'price': 0,
            'passing_score': 0, # No passing score for WAT
            'is_active': True,
            'created_by': admin_user
        }
    )
    
    if created:
        print(f"Created test: {test.name}")
    else:
        print(f"Using existing test: {test.name}")
        # Clear existing questions to re-seed if needed
        test.questions.all().delete()
        print("Cleared existing questions.")

    # 2. List of Words
    words = [
        "ANTIQUE", "OFFENSIVE", "CASTIGATION", "SQUALL", "PLEASURABLE", "CUSTODY", "RESCUE", "UTILIZE", "FIANCÉ", "SHUTTER",
        "RUB", "UNILATERAL", "ROTTER", "PROSECUTE", "MONASTIC", "HOUSEWIFE", "DISABLE", "MISFORTUNE", "REVOKE", "SATISFACTION",
        "SYMPTOM", "MESS", "QUALIFICATION", "HAUNT", "GESTURE", "DISAPPOINT", "DISASTER", "PARTY", "UTTER", "PAPER",
        "INACTIVE", "PUNCTUAL", "CIVILIZATION", "YOUNG", "SECULAR", "TERMINATE", "DILEMMA", "IRREGULAR", "NEST", "REVOLUTION",
        "SWEAT", "SUSPICIOUS", "TIDE", "TWIRL", "JEALOUS", "MEMORY", "DETERIORATE", "PARADE", "COMMAND", "PUNCH",
        "DOOM", "OBEY", "COMFORT", "BLOOD", "ACHIEVEMENT", "LORDSHIP", "MAJESTY", "REJECT", "NEGLECT", "HUMBLE",
        "FIRE", "SEX", "LITERATURE", "PLEASURE", "CREATIVE", "SINK", "SPEND", "WASTE", "TORTURE", "BOMB",
        "COLONEL", "DRAMA", "PROTEST", "BEAUTY", "SHOOT", "UNIFORM", "ETERNITY", "SEDUCE", "BEAT", "COLD"
    ]

    # 3. Create Questions
    questions_to_create = []
    for index, word in enumerate(words):
        question = Question(
            test=test,
            question_text=word,
            question_type='wat',
            difficulty_level='medium',
            order=index + 1,
            correct_answer="n/a", # Not applicable for WAT
            options=[], # No options for WAT
            explanation=""
        )
        questions_to_create.append(question)

    Question.objects.bulk_create(questions_to_create)
    print(f"Created {len(questions_to_create)} WAT questions.")
    
    # Update total questions count (signal might not trigger on bulk_create)
    test.total_questions = len(questions_to_create)
    test.save()
    print("Test updated successfully!")

if __name__ == "__main__":
    seed_wat_set1()
