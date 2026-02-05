from django.db import migrations

def update_test_duration(apps, schema_editor):
    Test = apps.get_model('tests', 'Test')
    # Update the newly created Set 3 to 9 minutes
    Test.objects.filter(name="Non-Verbal IQ Test - Set 3").update(duration_minutes=9)

class Migration(migrations.Migration):
    dependencies = [
        ('tests', '0007_seed_non_verbal_set3'),
    ]

    operations = [
        migrations.RunPython(update_test_duration),
    ]
