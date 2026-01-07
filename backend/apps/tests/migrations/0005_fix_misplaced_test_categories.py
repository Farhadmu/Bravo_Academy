from django.db import migrations

def fix_categories(apps, schema_editor):
    Test = apps.get_model('tests', 'Test')
    
    # 1. Fix WAT Tests
    # Move any test with "WAT" in the name to 'wat' category
    # (if not already there)
    updated_wat = Test.objects.filter(name__icontains="WAT").exclude(category='wat').update(category='wat')
    print(f"Updated {updated_wat} WAT tests to correct category.")
    
    # 2. Fix Non-Verbal Tests
    # Move any test with "Non-Verbal" in the name to 'non-verbal' category
    updated_nv = Test.objects.filter(name__icontains="Non-Verbal").exclude(category='non-verbal').update(category='non-verbal')
    print(f"Updated {updated_nv} Non-Verbal tests to correct category.")

class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0004_test_category'),
    ]

    operations = [
        migrations.RunPython(fix_categories),
    ]
