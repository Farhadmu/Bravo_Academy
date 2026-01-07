import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from apps.tests.models import Test

def fix_categories():
    print("Checking for miscategorized tests...")
    
    # 1. Fix WAT Tests
    # User says "5 sets of WAT tests" are in Verbal. 
    # We look for tests with "WAT" in the name that are NOT in 'wat' category.
    wat_tests = Test.objects.filter(name__icontains="WAT").exclude(category='wat')
    
    if wat_tests.exists():
        print(f"Found {wat_tests.count()} miscategorized WAT tests:")
        for test in wat_tests:
            print(f" - Moving '{test.name}' (Current: {test.category}) -> 'wat'")
            test.category = 'wat'
            test.save()
        print("✅ WAT tests moved successfully.")
    else:
        print("No miscategorized WAT tests found.")

    # 2. Fix Non-Verbal Tests
    # User says "Non-Verbal IQ Test - Set 1" is in Verbal.
    # We look for generic "Non-Verbal" in name to be safe, excluding already correct ones.
    nv_tests = Test.objects.filter(name__icontains="Non-Verbal").exclude(category='non-verbal')
    
    if nv_tests.exists():
        print(f"Found {nv_tests.count()} miscategorized Non-Verbal tests:")
        for test in nv_tests:
            print(f" - Moving '{test.name}' (Current: {test.category}) -> 'non-verbal'")
            test.category = 'non-verbal'
            test.save()
        print("✅ Non-Verbal tests moved successfully.")
    else:
        print("No miscategorized Non-Verbal tests found.")
        
    # Verify Final State
    print("\nFinal Category Counts:")
    print(f"Verbal: {Test.objects.filter(category='verbal').count()}")
    print(f"Non-Verbal: {Test.objects.filter(category='non-verbal').count()}")
    print(f"WAT: {Test.objects.filter(category='wat').count()}")

if __name__ == "__main__":
    fix_categories()
