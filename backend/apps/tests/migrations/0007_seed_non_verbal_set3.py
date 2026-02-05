from django.db import migrations
import os

def seed_non_verbal_set3(apps, schema_editor):
    Test = apps.get_model('tests', 'Test')
    Question = apps.get_model('questions', 'Question')
    User = apps.get_model('users', 'User')

    # 1. Get an admin user
    admin_user = User.objects.filter(is_superuser=True).first()
    if not admin_user:
        admin_user = User.objects.filter(role='admin').first()
    
    if not admin_user:
        # If absolutely no admin exists in prod yet (unlikely), skip to avoid crash
        return

    # 2. Create the Test
    test_name = "Non-Verbal IQ Test - Set 3"
    test, created = Test.objects.get_or_create(
        name=test_name,
        category='non-verbal',
        defaults={
            'description': "Advanced non-verbal reasoning and pattern recognition. Premium set featuring 28 complex problems.",
            'duration_minutes': 25,
            'total_questions': 28,
            'price': 0.00,
            'is_free_sample': False,
            'is_active': True,
            'created_by': admin_user
        }
    )

    if not created:
        # Re-seeding logic if necessary, but migrations usually run once
        return

    # 3. Data for 28 Questions
    questions_data = [
        {"text": "Geometric Shape Column Sequence", "ans": "a", "opts": ["Column: Hatched Triangle, Square, Circle, Black Triangle", "Column: Square, Black Triangle, Hatched Triangle, Circle", "Column: Hatched Triangle, Circle, Square, Black Triangle", "Column: Square, Hatched Triangle, Black Triangle, Circle", "Column: Black Triangle, Hatched Triangle, Square, Circle"]},
        {"text": "Binary Matrix (1-0) Pattern", "ans": "b", "opts": ["Matrix 4x4 binary sequence A", "Matrix 4x4 binary sequence B", "Matrix 4x4 binary sequence C", "Matrix 4x4 binary sequence D", "Matrix 4x4 binary sequence E"]},
        {"text": "Moving 4-Bar Oval Sequence", "ans": "e", "opts": ["Oval on Bar 1 & 2", "Oval on Bar 1 & 4", "Oval on Bar 2 & 4", "Oval on Bar 1 & 3", "Oval on Bar 2 & 3"]},
        {"text": "Nested Polygonal Sequence", "ans": "a", "opts": ["Trapezoid containing Hatched Triangle", "Hexagon containing Vertical Hatched Rectangle", "Diamond containing Downward Hatched Triangle", "Trapezoid containing Pentagon", "Pentagon containing Hatched Rectangle"]},
        {"text": "Grid-based Spatial Reasoning (Symbols moving)", "ans": "b", "opts": ["Grid: Top-Right Circle, Center Hatched Triangle, Bottom-Left L-shape", "Grid: Top-Right Circle, Center Hatched Triangle, Bottom-Left Corner", "Grid: Top-Right Black Circle, Center Hatched Triangle, Bottom-Left L-shape", "Grid: Top-Right Circle, Center White Triangle, Bottom-Left L-shape", "Grid: Top-Right Black Circle, Center Hatched Triangle, Bottom-Left Corner"]},
        {"text": "Shape, Color, and Internal Rectangle Sequence", "ans": "d", "opts": ["Dark Blue Circle with Horizontal White Rectangle", "White Diamond with Vertical Black Rectangle", "White Circle with Vertical Hatched Rectangle", "Dark Blue Circle with Vertical Hatched Rectangle", "Light Gray Hexagon with Horizontal Black Rectangle"]},
        {"text": "Symbolic Movement and Rotation (Star, Triangle, Circle)", "ans": "e", "opts": ["Circle (Top-Left), Triangle (Pointing Up), Star (Bottom-Right)", "Star (Top-Left), Triangle (Pointing Down), Circle (Bottom-Right)", "Central Triangle, Bottom-Right Circle with Star inside", "Star (Top-Right), Triangle (Pointing Left), Circle (Bottom-Right)", "Central Triangle (Pointing Down), Bottom-Right Circle with Star inside"]},
        {"text": "Odd One Out (Shape & Fill Consistency)", "ans": "d", "opts": ["Hatched Parallelogram with Black Rectangle", "Double-outlined Diamond with Gray fill", "V-Shape with Gray Square", "Hatched Trapezoid with White Triangle", "White Square with Black Rectangle"]},
        {"text": "Odd One Out (Count and Variation of Shapes)", "ans": "c", "opts": ["Cluster A", "Cluster B", "Cluster C", "Cluster D", "Cluster E"]},
        {"text": "Odd One Out (Grid Pattern Symmetry/Alignment)", "ans": "d", "opts": ["Grid A", "Grid B", "Grid C", "Grid D", "Grid E"]},
        {"text": "Odd One Out (Line Intersection Pattern)", "ans": "c", "opts": ["4 Vertical Lines intersected by 1 Horizontal", "2 Horizontal Lines intersected by 1 Slanted", "5 Vertical Lines intersected by 1 Slanted", "6 Vertical Lines intersected by 1 Slanted", "3 Horizontal Lines intersected by 1 Slanted"]},
        {"text": "Odd One Out (3D Block Rotation)", "ans": "a", "opts": ["Setup A", "Setup B", "Setup C", "Setup D", "Setup E"]},
        {"text": "Odd One Out (Nested Symbol Counts/Colors)", "ans": "e", "opts": ["Cluster A", "Cluster B", "Cluster C", "Cluster D", "Cluster E"]},
        {"text": "Odd One Out (Stack Symmetry)", "ans": "d", "opts": ["Stack A", "Stack B", "Stack C", "Stack D", "Stack E"]},
        {"text": "Set Classification (Set A vs Set B)", "ans": "b", "opts": ["Set A", "Set B", "Neither Set A nor Set B"]},
        {"text": "Set Classification (Dot Array)", "ans": "a", "opts": ["Set A", "Set B", "Neither Set A nor Set B"]},
        {"text": "Set Classification (Shape Clustering)", "ans": "c", "opts": ["Set A", "Set B", "Neither Set A nor Set B"]},
        {"text": "Set Classification (Nested Polygon)", "ans": "b", "opts": ["Set A", "Set B", "Neither Set A nor Set B"]},
        {"text": "Set Classification (Point Count)", "ans": "b", "opts": ["Set A", "Set B", "Neither Set A nor Set B"]},
        {"text": "Set Classification (Grid Alignment)", "ans": "b", "opts": ["Set A", "Set B", "Neither Set A nor Set B"]},
        {"text": "Set Classification (Spatial Distribution)", "ans": "c", "opts": ["Set A", "Set B", "Neither Set A nor Set B"]},
        {"text": "Applying Operations (Transformation)", "ans": "d", "opts": ["Option A", "Option B", "Option C", "Option D"]},
        {"text": "Applying Operations (Operator Selection)", "ans": "b", "opts": ["Operator A", "Operator B", "Operator C", "Operator D"]},
        {"text": "Applying Operations (Inverse Move)", "ans": "b", "opts": ["Box A", "Box B", "Box C", "Box D"]},
        {"text": "Applying Operations (Dual-Step)", "ans": "c", "opts": ["Result A", "Result B", "Result C", "Result D"]},
        {"text": "Applying Operations (Sequential Transformation)", "ans": "a", "opts": ["Diagram A", "Diagram B", "Diagram C", "Diagram D"]},
        {"text": "Applying Operations (Operator Mapping)", "ans": "d", "opts": ["Input A", "Input B", "Input C", "Input D"]},
        {"text": "Applying Operations (Operator Identification)", "ans": "b", "opts": ["Sequence A", "Sequence B", "Sequence C", "Sequence D"]}
    ]

    for i, q_data in enumerate(questions_data):
        options_json = [{'id': chr(97 + j), 'text': opt} for j, opt in enumerate(q_data["opts"])]
        Question.objects.create(
            test=test,
            question_text=q_data["text"],
            question_type='mcq',
            options=options_json,
            correct_answer=q_data["ans"],
            difficulty_level='hard',
            order=i + 1
        )

class Migration(migrations.Migration):
    dependencies = [
        ('tests', '0006_seed_sample_test'),
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_non_verbal_set3),
    ]
