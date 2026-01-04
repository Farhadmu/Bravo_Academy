
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

def seed_wat_set4():
    print("Seeding WAT Set 4 (Corrected List)...")
    
    # 1. Create or Get the Test
    admin_user = User.objects.filter(is_superuser=True).first()
    if not admin_user:
        print("Error: No admin user found. Please create one.")
        return

    test_name = "WAT Set 4"
    
    # Corrected words provided by user
    # Note: Cleaned up "(Corrected from...)" notes
    words = [
        "DISCUSSION", "SYSTEM", "QUICK", "DREADFUL", "CAUSE", "GAY", "SPECIFIC", "METHOD", "HUNGER", "GREED",
        "ILL", "KINDNESS", "CRITICISM", "GREATNESS", "COMPROMISE", "WORD", "PERSUADE", "CONFUSION", "AFFECTION", "REQUEST",
        "DEPRESSION", "DEFEAT", "FATHER", "KNOWLEDGE", "ENTERTAINMENT", "LAUGHTER", "EDUCATION", "COURAGE", "QUANTITY", "MISER",
        "INSANE", "CHANGE", "PRECAUTION", "POLITENESS", "BABY", "CLERK", "EXCUSE", "FAULT", "VIRGIN", "MURDERER",
        "RESPONSE", "DESIGNATION", "MOBILE", "LEADERSHIP", "OVERCONFIDENCE", "VULGAR", "HIJACKING", "NATIVE", "PROFESSION", "ACTION",
        "PROSPER", "CHANGE", "VICTORY", "DISOBEY", "COURAGE", "SETTLEMENT", "DISTINCTION", "FRAUGHT", "WORK", "AMBITION",
        "COMPLAINT", "ENJOYMENT", "OBEDIENCE", "DIAGNOSE", "KILL", "AFFECTION", "ESPRIT", "WOOLLEN", "VICTIM", "RADIANCE",
        "ETIQUETTE", "WHISKY", "THESAURUS", "AGILE", "DUMB", "RESPECT", "BORDER", "SENIOR", "DOMINANT", "SWORD"
    ]
    
    # Count: 80 words
    count = len(words)
    # Duration: 80 * 10s = 800s = 13.33 mins. Set 14 for buffer.
    duration = 14
    
    test, created = Test.objects.get_or_create(
        name=test_name,
        defaults={
            'description': f"Word Association Test Set 4. You will see {count} words, one by one, for 10 seconds each.",
            'duration_minutes': duration, 
            'total_questions': count,
            'price': 0,
            'passing_score': 0, 
            'is_active': True,
            'created_by': admin_user
        }
    )
    
    if not created:
        print(f"Updating existing test: {test.name}")
        # Update metadata if needed
        test.description = f"Word Association Test Set 4. You will see {count} words, one by one, for 10 seconds each."
        test.total_questions = count
        test.save()
        
        # Clear existing questions to re-seed if needed
        test.questions.all().delete()
        print("Cleared existing questions.")
    else:
        print(f"Created test: {test.name}")

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
    seed_wat_set4()
