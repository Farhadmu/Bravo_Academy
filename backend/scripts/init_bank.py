import os
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
django.setup()

from apps.tests.models import Test
from apps.questions.models import Question

def init_bank():
    try:
        test = Test.objects.get(name='IQ Test - Set 1')
        test.is_bank = True
        test.total_questions = 1000 # Supporting up to 10 sets of 100
        test.save()
        print(f"Test '{test.name}' marked as BANK.")
        
        questions = Question.objects.filter(test=test).order_by('order')
        for i, q in enumerate(questions):
            q.bank_order = i + 1
            q.save()
        print(f"Updated {questions.count()} questions with bank_order.")
    except Test.DoesNotExist:
        print("Test 'IQ Test - Set 1' not found.")

if __name__ == "__main__":
    init_bank()
