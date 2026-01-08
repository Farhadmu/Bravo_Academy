from django.db import migrations

def seed_non_verbal_q21_25(apps, schema_editor):
    Test = apps.get_model('tests', 'Test')
    Question = apps.get_model('questions', 'Question')
    QuestionImage = apps.get_model('questions', 'QuestionImage')

    test_name = "Non-Verbal IQ Test - Set 2"
    test = Test.objects.filter(name=test_name).first()
    if not test:
        test = Test.objects.filter(category='non-verbal').filter(name__contains='Set 2').first()
    
    if not test:
        print(f"Skipping migration: Test '{test_name}' not found.")
        return

    questions_data = [
        {
            "order": 21,
            "image_file": "non_verbal_q21.png", 
            "answer": "c", 
            "explanation": "The number of objects increases by 1 at each step from left to right in each row."
        },
        {
            "order": 22,
            "image_file": "non_verbal_q22.png",
            "answer": "a",
            "explanation": "In each row, the circle appears in three states: unshaded, upper part shaded, and right-hand side (RHS) part shaded. There are three different positions for the two triangles, each used only once per row. Also, two of the three figures in each row have one shaded triangle."
        },
        {
            "order": 23,
            "image_file": "non_verbal_q23.png",
            "answer": "d",
            "explanation": "The central line moves 90° clockwise in each step. The small line and the small circle interchange their positions in each step. The number of small circles increases by one at each step."
        },
        {
            "order": 24,
            "image_file": "non_verbal_q24.png",
            "answer": "d",
            "explanation": "The line inside the square moves from one corner to another in a clockwise direction as you move from left to right in a row."
        },
        {
            "order": 25,
            "image_file": "non_verbal_q25.png",
            "answer": "a",
            "explanation": "The third figure in each row comprises the parts which are not common to the first two figures."
        }
    ]

    for q_data in questions_data:
        # Avoid duplicates
        if Question.objects.filter(test=test, order=q_data["order"]).exists():
            continue

        question = Question.objects.create(
            test=test,
            question_text=f"Identify the missing figure in the pattern (Question {q_data['order']})",
            question_type="mcq",
            difficulty_level="medium",
            correct_answer=q_data["answer"],
            explanation=q_data["explanation"],
            order=q_data["order"],
            options=[
                {"id": "a", "text": "Figure a"},
                {"id": "b", "text": "Figure b"},
                {"id": "c", "text": "Figure c"},
                {"id": "d", "text": "Figure d"}
            ]
        )
        
        # Link S3 Image
        s3_key = f"questions/seeds/{q_data['image_file']}"
        QuestionImage.objects.create(
            question=question,
            image=s3_key, 
            caption="Question Figure"
        )

    # Re-sync total_questions
    actual_count = Question.objects.filter(test=test).count()
    test.total_questions = actual_count
    test.save()

def remove_seeds(apps, schema_editor):
    Question = apps.get_model('questions', 'Question')
    Test = apps.get_model('tests', 'Test')
    test = Test.objects.filter(name="Non-Verbal IQ Test - Set 2").first()
    if test:
        Question.objects.filter(test=test, order__range=(21, 25)).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0007_seed_non_verbal_set2_q16_20'),
    ]

    operations = [
        migrations.RunPython(seed_non_verbal_q21_25, remove_seeds),
    ]
