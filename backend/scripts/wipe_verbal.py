import os
import django
import sys

# Setup Django environment
sys.path.append('/var/www/online-edu/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
django.setup()

from apps.questions.models import Question
from apps.tests.models import Test

def wipe_verbal_data():
    print("Starting Verbal IQ Data Wipe...")
    
    # 1. Identify Verbal Tests
    verbal_tests = Test.objects.filter(category='verbal')
    print(f"Found {verbal_tests.count()} Verbal IQ tests.")
    
    # 2. Wipe Questions
    # Update correct_answer to empty string or a safe dummy value
    # Update explanation to empty string
    updated = Question.objects.filter(test__in=verbal_tests).update(
        correct_answer='REMOVED', 
        explanation=''
    )
    
    print(f"Successfully wiped answers and explanations for {updated} questions.")
    
if __name__ == '__main__':
    wipe_verbal_data()
