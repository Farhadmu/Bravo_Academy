import os
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
django.setup()

from apps.tests.models import Test
from apps.questions.models import Question

def revert_to_sets():
    try:
        # 1. Update Set 1
        set1 = Test.objects.filter(is_bank=True).first()
        if not set1:
             print("Set 1 bank not found. Looking for 'IQ Test - Set 1'...")
             set1 = Test.objects.filter(name="IQ Test - Set 1").first()
        
        if not set1:
            print("Set 1 not found. Creating Set 1...")
            set1 = Test.objects.create(
                name="IQ Test - Set 1",
                duration_minutes=30,
                total_questions=100,
                price=0.00,
                is_free_sample=True,
                is_bank=False
            )
        else:
            print(f"Updating {set1.name}...")
            set1.is_bank = False
            set1.is_free_sample = True
            set1.total_questions = 100
            set1.save()

        # 2. Create Set 2
        set2, created = Test.objects.get_or_create(
            name="IQ Test - Set 2",
            defaults={
                "duration_minutes": 30,
                "total_questions": 100,
                "price": 0.00,
                "is_free_sample": False,
                "is_bank": False
            }
        )
        if created:
            print("Created IQ Test - Set 2.")
        else:
            print("IQ Test - Set 2 already exists.")
            set2.total_questions = 100
            set2.is_bank = False
            set2.save()

        # 3. Re-link questions
        print("Re-linking questions...")
        # Questions 1-100 stay with set1
        q_set1_count = Question.objects.filter(test=set1, bank_order__lte=100).update(test=set1)
        print(f"Linked {q_set1_count} questions to Set 1.")
        
        # Questions 101-200 move to set2
        # We also need to update their 'order' field to be sequential within the new test
        q_set2 = Question.objects.filter(bank_order__gt=100).order_by('bank_order')
        q_set2_count = 0
        for q in q_set2:
            q.test = set2
            q_set2_count += 1
            q.order = q_set2_count
            q.save()
        
        print(f"Moved {q_set2_count} questions to Set 2.")

        # 4. Cleanup Set 1 orders
        q_set1 = Question.objects.filter(test=set1).order_by('bank_order')
        for i, q in enumerate(q_set1, 1):
            q.order = i
            q.save()

        print("Migration complete.")
        
    except Exception as e:
        print(f"Error during migration: {e}")

if __name__ == "__main__":
    revert_to_sets()
