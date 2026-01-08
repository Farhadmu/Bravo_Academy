from django.db import migrations

def seed_non_verbal_q6_10(apps, schema_editor):
    Test = apps.get_model('tests', 'Test')
    Question = apps.get_model('questions', 'Question')
    QuestionImage = apps.get_model('questions', 'QuestionImage')

    test_name = "Non-Verbal IQ Test - Set 2"
    test = Test.objects.filter(name=test_name).first()
    
    if not test:
        # Fallback if first part didn't run or name is slightly different
        test = Test.objects.filter(category='non-verbal').filter(name__contains='Set 2').first()
    
    if not test:
        print(f"Skipping migration: Test '{test_name}' not found.")
        return

    questions_data = [
        {
            "order": 6,
            "image_file": "non_verbal_q6.png", 
            "answer": "d", 
            "explanation": "In each row, the third figure is a collection of the common elements (line segments) of the first and the second figures."
        },
        {
            "order": 7,
            "image_file": "non_verbal_q7.png",
            "answer": "c",
            "explanation": "In each row, there are three types of arrows: an arrow with a single head and no base, an arrow with a double head and a circle at its base, and an arrow with a triple head and a rectangle at its base. Additionally, in each row, the arrows point in three directions: upwards, downwards, and towards the right."
        },
        {
            "order": 8,
            "image_file": "non_verbal_q8.png",
            "answer": "b",
            "explanation": "In each row, the second figure is obtained by removing the outermost element of the first figure, and the third figure is obtained by removing the outermost element of the second figure."
        },
        {
            "order": 9,
            "image_file": "non_verbal_q9.png",
            "answer": "c",
            "explanation": "There are three types of faces, three types of hands, and three types of legs. Each type is used once in each row. Therefore, the missing figure in the third row is formed by combining the features not used in the first two figures of that row."
        },
        {
            "order": 10,
            "image_file": "non_verbal_q10.png",
            "answer": "d",
            "explanation": "In each row, from left to right, the directions of the elements are changing, and the quantities of elements are either increasing or decreasing."
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
        Question.objects.filter(test=test, order__range=(6, 10)).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0004_clear_verbal_answers'),
    ]

    operations = [
        migrations.RunPython(seed_non_verbal_q6_10, remove_seeds),
    ]
