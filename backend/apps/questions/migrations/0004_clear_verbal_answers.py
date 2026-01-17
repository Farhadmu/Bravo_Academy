from django.db import migrations

def clear_verbal_answers(apps, schema_editor):
    """
    Clears correct_answer and explanation for all Verbal IQ questions.
    Sets correct_answer to 'PENDING' to effectively 'remove' the wrong answer
    until the user provides the correct ones.
    """
    Test = apps.get_model('tests', 'Test')
    Question = apps.get_model('questions', 'Question')
    
    # 1. Find all Verbal IQ tests
    verbal_tests = Test.objects.filter(category='verbal')
    
    # 2. Update questions for these tests
    # We set correct_answer to a placeholder that won't match any option ID (usually 'a', 'b', 'c', 'd')
    updated_count = Question.objects.filter(test__in=verbal_tests).update(
        correct_answer='PENDING',
        explanation=''
    )
    
    print(f"Cleared answers and explanations for {updated_count} Verbal IQ questions.")

def reverse_clear(apps, schema_editor):
    # We cannot restore the old wrong answers easily without a backup, 
    # and we don't want to.
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0003_alter_question_options_question_bank_order_and_more'),
        ('tests', '0004_test_category'),
    ]

    operations = [
        migrations.RunPython(clear_verbal_answers, reverse_clear),
    ]
