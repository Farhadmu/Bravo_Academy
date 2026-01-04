
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

def seed_wat_set5():
    print("Seeding WAT Set 5...")
    
    # 1. Create or Get the Test
    admin_user = User.objects.filter(is_superuser=True).first()
    if not admin_user:
        print("Error: No admin user found. Please create one.")
        return

    test_name = "WAT Set 5"
    
    # Words provided by user
    words = [
        "WREAK", "REFRAIN", "CONCEAL", "ANNOYS", "MOURN", "INTREPIDITY", "PATERNAL", "VENTUROUS", "MONOGRAM", "LIE",
        "POISON", "TENSION", "TRAITOR", "UPSET", "AWFUL", "REVENGE", "FRIGHT", "NEVER", "POVERTY", "BATTLE",
        "BULLY", "BONDAGE", "POPULOUS", "ALTERATION", "POPULARITY", "DISBELIEVE", "SOLVE", "DISAPPROVAL", "DISABILITY", "BRUTAL",
        "ADJUDGEMENT", "BRAVERY", "AFTERMATH", "BRUSHWOOD", "CONDUCT", "FORMALIN", "CLASSIFICATION", "FOUL", "RAPID", "MANUFACTURE",
        "RECOGNITION", "CHESS", "PRESENT", "AMBITION", "DISCOURAGING", "REBEL", "PRESIDENT", "RESCUE", "TEMPORARY", "QUIP",
        "RECITE", "RECTIFY", "RELIEVE", "SEVERE", "DANCE", "WORTH", "AFFECTION", "THRILL", "TORTURE", "REFRAIN",
        "ATTACK", "TREE", "HATE", "STEAL", "RELATION", "ANXIOUS", "BILATERAL", "HUNGER", "DEMURRAGE", "DISTINCT",
        "POWER", "ACCOMPLISH", "BARRIER", "CRUEL", "BOREDOM", "FATIGUE", "CULPABLE", "HAZY", "EFFICIENCY", "CHILDISH"
    ]
    
    # Count: 80 words
    count = len(words)
    # Duration: 80 * 10s = 800s = 13.33 mins. Set 14 for buffer.
    duration = 14
    
    test, created = Test.objects.get_or_create(
        name=test_name,
        defaults={
            'description': f"Word Association Test Set 5. You will see {count} words, one by one, for 10 seconds each.",
            'duration_minutes': duration, 
            'total_questions': count,
            'price': 0,
            'passing_score': 0, 
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

    # 3. Create Questions
    questions_to_create = []
    for index, word in enumerate(words):
        question = Question(
            test=test,
            question_text=word,
            question_type='wat',
            difficulty_level='medium',
            order=index + 1,
            correct_answer="n/a", 
            options=[],
            explanation=""
        )
        questions_to_create.append(question)

    Question.objects.bulk_create(questions_to_create)
    print(f"Created {len(questions_to_create)} WAT questions.")
    
    # Update total questions count
    test.total_questions = len(questions_to_create)
    test.save()
    print("Test updated successfully!")

if __name__ == "__main__":
    seed_wat_set5()
