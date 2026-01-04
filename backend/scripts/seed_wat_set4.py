
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
    print("Seeding WAT Set 4...")
    
    # 1. Create or Get the Test
    admin_user = User.objects.filter(is_superuser=True).first()
    if not admin_user:
        print("Error: No admin user found. Please create one.")
        return

    test_name = "WAT Set 4"
    
    # Words provided by user
    words = [
        "Booze", "Suspect", "Worthless", "Appreciate", "Episode", "Insensitive", "Kite", "Liability", 
        "Pole", "Adventure", "Army", "Adversity", "Cooperation", "Congratulation", "Discourage", 
        "Examination", "Dictator", "Illiterate", "Lively", "Opposition", "Company", "Mutation", 
        "Expected", "Trembling", "Influence", "Punishment", "Stranger", "Character", "Misunderstanding", 
        "Blunder", "Peace", "Charm", "Aggregate", "Compose", "Stick", "Sweep", "Conflict", "Blow", 
        "Shine", "Money", "Faith", "Revenge", "Impossible", "Gossip", "Blueprint", "Confuse", 
        "Discipline", "Freedom", "Democracy", "Confidence", "Evening", "Groom", "Efficiency", 
        "Designation", "Bitter", "Supreme", "Culprit", "Conquer", "Advantage", "Objection", 
        "Insurance", "Leopard", "Patriotism", "Philosophy", "Carelessness", "Aggressive", "Heritage", 
        "Punctuality", "Assist", "Initiation", "Advertisement", "Withdraw", "Angry", "Fallow", 
        "Inspection", "Graduate", "Tidy", "Convince", "Character", "Influence"
    ]
    
    # Convert to UPPERCASE to match previous sets style? User provided Title Case.
    # Previous sets were all caps. I should probably convert to UPPER for consistency 
    # OR keep as user provided. 
    # The user provided list for Set 3 was UPPERCASE. Set 2 was UPPERCASE.
    # Set 4 input is Title Case. 
    # I will convert to UPPERCASE for consistency with other sets.
    words = [w.upper() for w in words]
    
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
    seed_wat_set4()
