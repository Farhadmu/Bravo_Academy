
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

def seed_wat_set2():
    print("Seeding WAT Set 2...")
    
    # 1. Create or Get the Test
    admin_user = User.objects.filter(is_superuser=True).first()
    if not admin_user:
        print("Error: No admin user found. Please create one.")
        return

    test_name = "WAT Set 2"
    
    # Words provided by user
    words = [
        "SWORD", "YOUTH", "HESITATION", "ESCAPE", "ENTERTAIN", "DEFEAT", "DIMINISH", "REQUEST", "FAULT", "INSENSITIVE",
        "JUSTICE", "IMPULSIVE", "MERCY", "OPTIMISTIC", "AFFECTION", "LOYALTY", "POLITICAL", "COMPANY", "INSULT", "OUTCOME",
        "CRISIS", "IMAGINATION", "MURDER", "CHANGE", "DESIGNATION", "MISTAKE", "SENIOR", "DISAGREE", "KEEN", "DIVERSITY",
        "EXTRAORDINARY", "EFFICIENCY", "HUMOROUS", "AMBITIOUS", "ARGUMENT", "AMBASSADOR", "SETTLEMENT", "BEGGAR", "RESPECT", "DRUG",
        "VIOLENCE", "ARROGANCE", "DEATH", "FANTASY", "AFFAIR", "CIRCUMSTANCES", "CLERK", "GALLANT", "WHISKY", "INITIATIVE",
        "KILL", "RELIGION", "MATURE", "VICTIM", "SUSPENSE", "TECHNOLOGY", "TRANSPARENT", "WITHDRAW", "VIRGIN", "NATIVE",
        "NIGHTMARE", "MACHINE", "FOLLOW", "PRECAUTION", "HASTE"
    ]
    
    # Calculate duration: 65 words * 10s = 650s approx 10.8 mins, set 12 for buffer
    # Note: User provided 65 words in the list above (manual count for validation)
    
    test, created = Test.objects.get_or_create(
        name=test_name,
        defaults={
            'description': f"Word Association Test Set 2. You will see {len(words)} words, one by one, for 10 seconds each.",
            'duration_minutes': 12, 
            'total_questions': len(words),
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
    seed_wat_set2()
