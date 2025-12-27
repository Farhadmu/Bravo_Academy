import os
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
django.setup()

from apps.tests.models import Test
from apps.questions.models import Question

def fix_set1_errors():
    """Fix identified errors in Set 1."""
    
    set1 = Test.objects.get(name='IQ Test - Set 1')
    
    # Fix Q87: LSARBIA → BARISAL, 4th letter should be I (not R)
    q87 = Question.objects.filter(test=set1, bank_order=87).first()
    if q87:
        print(f"Fixing Q87: LSARBIA → BARISAL")
        print(f"Current correct answer: {q87.correct_answer}")
        
        # Find option with 'I'
        for opt in q87.options:
            if opt['text'] == 'I':
                print(f"Changing correct answer to: {opt['id']} = I")
                q87.correct_answer = opt['id']
                q87.explanation = "The word is BARISAL. 4th letter (B-A-R-I) is I."
                q87.save()
                print("✓ Fixed Q87!")
                break
    
    print("\nAll errors fixed!")

if __name__ == "__main__":
    fix_set1_errors()
