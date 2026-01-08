from django.db import migrations

def seed_non_verbal_q11_15(apps, schema_editor):
    Test = apps.get_model('tests', 'Test')
    Question = apps.get_model('questions', 'Question')
    QuestionImage = apps.get_model('questions', 'QuestionImage')

    test_name = "Non-Verbal IQ Test - Set 2"
    # Use the same fallback/lookup logic as before
    test = Test.objects.filter(name=test_name).first()
    if not test:
        test = Test.objects.filter(category='non-verbal').filter(name__contains='Set 2').first()
    
    if not test:
        print(f"Skipping migration: Test '{test_name}' not found.")
        return

    questions_data = [
        {
            "order": 11,
            "image_file": "non_verbal_q11.png", 
            "answer": "c", 
            "explanation": "The number of components in each row either increases or decreases from left to right. In the third row, the number increases."
        },
        {
            "order": 12,
            "image_file": "non_verbal_q12.png",
            "answer": "d",
            "explanation": "In each row, the second figure is obtained by rotating the first figure through 90° clockwise (CW) or 90° anticlockwise (ACW) and adding a circle to it. The third figure is obtained by adding two circles to the first figure without rotating it."
        },
        {
            "order": 13,
            "image_file": "non_verbal_q13.png",
            "answer": "d",
            "explanation": "The third figure in each row comprises the parts which are not common to the first two figures."
        },
        {
            "order": 14,
            "image_file": "non_verbal_q14.png",
            "answer": "a",
            "explanation": "The second figure is a part of the first figure (but is not exactly the same as the first figure)."
        },
        {
            "order": 15,
            "image_file": "non_verbal_q15.png",
            "answer": "c",
            "explanation": "In each row, all three shapes—triangle, square, and pentagon—are present."
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

    # Re-sync total_questions (though signals should handle it, let's be explicit)
    actual_count = Question.objects.filter(test=test).count()
    test.total_questions = actual_count
    test.save()

def remove_seeds(apps, schema_editor):
    Question = apps.get_model('questions', 'Question')
    Test = apps.get_model('tests', 'Test')
    test = Test.objects.filter(name="Non-Verbal IQ Test - Set 2").first()
    if test:
        Question.objects.filter(test=test, order__range=(11, 15)).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0005_seed_non_verbal_set2_q6_10'),
    ]

    operations = [
        migrations.RunPython(seed_non_verbal_q11_15, remove_seeds),
    ]
