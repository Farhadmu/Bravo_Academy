from django.db import migrations

def seed_non_verbal_q16_20(apps, schema_editor):
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
            "order": 16,
            "image_file": "non_verbal_q16.png", 
            "answer": "b", 
            "explanation": "In each row, the number of dots in the second figure is three times (thrice) the number in the first figure."
        },
        {
            "order": 17,
            "image_file": "non_verbal_q17.png",
            "answer": "d",
            "explanation": "The number of each type of figure decreases by 1 at each step from left to right in each row."
        },
        {
            "order": 18,
            "image_file": "non_verbal_q18.png",
            "answer": "a",
            "explanation": "The third figure in each row comprises the parts that are common to the first two figures."
        },
        {
            "order": 19,
            "image_file": "non_verbal_q19.png",
            "answer": "c",
            "explanation": "In the first and third columns, the black portion of the middle image is diagonally opposite to that of the lower image. Therefore, the middle image in the second column must follow the same pattern, as shown in the correct answer."
        },
        {
            "order": 20,
            "image_file": "non_verbal_q20.png",
            "answer": "b",
            "explanation": "In each row, the shapes follow a consistent sequence: triangle follows circle, square follows triangle, and circle follows square. For the third row, this rule applies to both the inner and the outer elements of the figures."
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
        Question.objects.filter(test=test, order__range=(16, 20)).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0006_seed_non_verbal_set2_q11_15'),
    ]

    operations = [
        migrations.RunPython(seed_non_verbal_q16_20, remove_seeds),
    ]
