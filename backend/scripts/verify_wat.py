
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

from apps.tests.models import Test
from apps.questions.models import Question

def verify_wat():
    print("Verifying WAT Set 5...")
    try:
        test = Test.objects.get(name="WAT Set 5")
        print(f"Test Found: {test.name}")
        print(f"Active: {test.is_active}")
        
        real_count = Question.objects.filter(test=test).count()
        
        if real_count == 80:
            print("SUCCESS: 80 questions confirmed.")
        else:
            print(f"FAILURE: Expected 80 questions, found {real_count}")

        # Check first question type
        first_q = test.questions.first()
        if first_q:
             print(f"Sample Question Type: {first_q.question_type}")
             if first_q.question_type == 'wat':
                 print("SUCCESS: Question type is 'wat'")
             else:
                 print(f"FAILURE: Question type is {first_q.question_type}")

    except Test.DoesNotExist:
        print("FAILURE: Test 'WAT Set 1' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    verify_wat()
