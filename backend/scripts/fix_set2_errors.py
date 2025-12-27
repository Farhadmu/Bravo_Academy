import os
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
django.setup()

from apps.tests.models import Test
from apps.questions.models import Question

def fix_set2_errors():
    """Fix identified errors in Set 2."""
    
    set2 = Test.objects.get(name='IQ Test - Set 2')
    
    # Fix Q152: SSIEZRLORSC → SCISSORS, 6th letter should be O (not R)
    q152 = Question.objects.filter(test=set2, bank_order=152).first()
    if q152:
        print(f"Fixing Q152: SSIEZRLORSC → SCISSORS")
        print(f"Current correct answer: {q152.correct_answer}")
        print(f"Question: {q152.question_text}")
        
        # Find option with 'O'
        for opt in q152.options:
            if opt['text'] == 'O':
                print(f"Changing correct answer to: {opt['id']} = O")
                q152.correct_answer = opt['id']
                q152.explanation = "The word is SCISSORS. 6th letter (S-C-I-S-S-O) is O."
                q152.save()
                print("✓ Fixed Q152!")
                break
    
    print("\nAll Set 2 errors fixed!")

if __name__ == "__main__":
    fix_set2_errors()
