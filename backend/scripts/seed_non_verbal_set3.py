import os
import sys
import django
from pathlib import Path

# Setup Django environment
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, 'apps'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
django.setup()

from apps.tests.models import Test
from apps.questions.models import Question, QuestionImage
from apps.users.models import User
from django.core.files import File

def seed_nv_set3():
    print("🚀 Starting Seeding: Non-Verbal IQ Test - Set 3 (Premium)")
    
    # 1. Get or create a superuser for 'created_by'
    admin_user = User.objects.filter(is_superuser=True).first()
    if not admin_user:
        admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("✅ Created superuser: admin")

    # 2. Create or Get "Non-Verbal IQ Test - Set 3"
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
        # Clear existing questions for fresh seed
        test.questions.all().delete()
        print(f"🗑️ Cleared existing questions for '{test_name}'")
    else:
        print(f"✨ Created new test: {test_name}")

    # 3. Define 28 Questions
    questions_data = [
        {
            "text": "Geometric Shape Column Sequence",
            "ans": "a",
            "opts": ["Column: Hatched Triangle, Square, Circle, Black Triangle", "Column: Square, Black Triangle, Hatched Triangle, Circle", "Column: Hatched Triangle, Circle, Square, Black Triangle", "Column: Square, Hatched Triangle, Black Triangle, Circle", "Column: Black Triangle, Hatched Triangle, Square, Circle"],
            "img": "nv3_q1.png"
        },
        {
            "text": "Binary Matrix (1-0) Pattern",
            "ans": "b",
            "opts": ["Matrix 4x4 binary sequence A", "Matrix 4x4 binary sequence B", "Matrix 4x4 binary sequence C", "Matrix 4x4 binary sequence D", "Matrix 4x4 binary sequence E"],
            "img": "nv3_q2.png"
        },
        {
            "text": "Moving 4-Bar Oval Sequence",
            "ans": "e",
            "opts": ["Oval on Bar 1 & 2", "Oval on Bar 1 & 4", "Oval on Bar 2 & 4", "Oval on Bar 1 & 3", "Oval on Bar 2 & 3"],
            "img": "nv3_q3.png"
        },
        {
            "text": "Nested Polygonal Sequence",
            "ans": "a",
            "opts": ["Trapezoid containing Hatched Triangle", "Hexagon containing Vertical Hatched Rectangle", "Diamond containing Downward Hatched Triangle", "Trapezoid containing Pentagon", "Pentagon containing Hatched Rectangle"],
            "img": "nv3_q4.png"
        },
        {
            "text": "Grid-based Spatial Reasoning (Symbols moving)",
            "ans": "b",
            "opts": ["Grid: Top-Right Circle, Center Hatched Triangle, Bottom-Left L-shape", "Grid: Top-Right Circle, Center Hatched Triangle, Bottom-Left Corner", "Grid: Top-Right Black Circle, Center Hatched Triangle, Bottom-Left L-shape", "Grid: Top-Right Circle, Center White Triangle, Bottom-Left L-shape", "Grid: Top-Right Black Circle, Center Hatched Triangle, Bottom-Left Corner"],
            "img": "nv3_q5.png"
        },
        {
            "text": "Shape, Color, and Internal Rectangle Sequence",
            "ans": "d",
            "opts": ["Dark Blue Circle with Horizontal White Rectangle", "White Diamond with Vertical Black Rectangle", "White Circle with Vertical Hatched Rectangle", "Dark Blue Circle with Vertical Hatched Rectangle", "Light Gray Hexagon with Horizontal Black Rectangle"],
            "img": "nv3_q6.png"
        },
        {
            "text": "Symbolic Movement and Rotation (Star, Triangle, Circle)",
            "ans": "e",
            "opts": ["Circle (Top-Left), Triangle (Pointing Up), Star (Bottom-Right)", "Star (Top-Left), Triangle (Pointing Down), Circle (Bottom-Right)", "Central Triangle, Bottom-Right Circle with Star inside", "Star (Top-Right), Triangle (Pointing Left), Circle (Bottom-Right)", "Central Triangle (Pointing Down), Bottom-Right Circle with Star inside"],
            "img": "nv3_q7.png"
        },
        {
            "text": "Odd One Out (Shape & Fill Consistency)",
            "ans": "d",
            "opts": ["Hatched Parallelogram with Black Rectangle", "Double-outlined Diamond with Gray fill", "V-Shape with Gray Square", "Hatched Trapezoid with White Triangle", "White Square with Black Rectangle"],
            "img": "nv3_q8.png"
        },
        {
            "text": "Odd One Out (Count and Variation of Shapes)",
            "ans": "c",
            "opts": ["Cluster A", "Cluster B", "Cluster C", "Cluster D", "Cluster E"],
            "img": "nv3_q9.png"
        },
        {
            "text": "Odd One Out (Grid Pattern Symmetry/Alignment)",
            "ans": "d",
            "opts": ["Grid A", "Grid B", "Grid C", "Grid D", "Grid E"],
            "img": "nv3_q10.png"
        },
        {
            "text": "Odd One Out (Line Intersection Pattern)",
            "ans": "c",
            "opts": ["4 Vertical Lines intersected by 1 Horizontal", "2 Horizontal Lines intersected by 1 Slanted", "5 Vertical Lines intersected by 1 Slanted", "6 Vertical Lines intersected by 1 Slanted", "3 Horizontal Lines intersected by 1 Slanted"],
            "img": "nv3_q11.png"
        },
        {
            "text": "Odd One Out (3D Block Rotation)",
            "ans": "a",
            "opts": ["Setup A", "Setup B", "Setup C", "Setup D", "Setup E"],
            "img": "nv3_q12.png"
        },
        {
            "text": "Odd One Out (Nested Symbol Counts/Colors)",
            "ans": "e",
            "opts": ["Cluster A", "Cluster B", "Cluster C", "Cluster D", "Cluster E"],
            "img": "nv3_q13.png"
        },
        {
            "text": "Odd One Out (Stack Symmetry)",
            "ans": "d",
            "opts": ["Stack A", "Stack B", "Stack C", "Stack D", "Stack E"],
            "img": "nv3_q14.png"
        },
        {
            "text": "Set Classification (Set A vs Set B)",
            "ans": "b",
            "opts": ["Set A", "Set B", "Neither Set A nor Set B"],
            "img": "nv3_q15.png"
        },
        {
            "text": "Set Classification (Dot Array)",
            "ans": "a",
            "opts": ["Set A", "Set B", "Neither Set A nor Set B"],
            "img": "nv3_q16.png"
        },
        {
            "text": "Set Classification (Shape Clustering)",
            "ans": "c",
            "opts": ["Set A", "Set B", "Neither Set A nor Set B"],
            "img": "nv3_q17.png"
        },
        {
            "text": "Set Classification (Nested Polygon)",
            "ans": "b",
            "opts": ["Set A", "Set B", "Neither Set A nor Set B"],
            "img": "nv3_q18.png"
        },
        {
            "text": "Set Classification (Point Count)",
            "ans": "b",
            "opts": ["Set A", "Set B", "Neither Set A nor Set B"],
            "img": "nv3_q19.png"
        },
        {
            "text": "Set Classification (Grid Alignment)",
            "ans": "b",
            "opts": ["Set A", "Set B", "Neither Set A nor Set B"],
            "img": "nv3_q20.png"
        },
        {
            "text": "Set Classification (Spatial Distribution)",
            "ans": "c",
            "opts": ["Set A", "Set B", "Neither Set A nor Set B"],
            "img": "nv3_q21.png"
        },
        {
            "text": "Applying Operations (Transformation)",
            "ans": "d",
            "opts": ["Option A", "Option B", "Option C", "Option D"],
            "img": "nv3_q22.png"
        },
        {
            "text": "Applying Operations (Operator Selection)",
            "ans": "b",
            "opts": ["Operator A", "Operator B", "Operator C", "Operator D"],
            "img": "nv3_q23.png"
        },
        {
            "text": "Applying Operations (Inverse Move)",
            "ans": "b",
            "opts": ["Box A", "Box B", "Box C", "Box D"],
            "img": "nv3_q24.png"
        },
        {
            "text": "Applying Operations (Dual-Step)",
            "ans": "c",
            "opts": ["Result A", "Result B", "Result C", "Result D"],
            "img": "nv3_q25.png"
        },
        {
            "text": "Applying Operations (Sequential Transformation)",
            "ans": "a",
            "opts": ["Diagram A", "Diagram B", "Diagram C", "Diagram D"],
            "img": "nv3_q26.png"
        },
        {
            "text": "Applying Operations (Operator Mapping)",
            "ans": "d",
            "opts": ["Input A", "Input B", "Input C", "Input D"],
            "img": "nv3_q27.png"
        },
        {
            "text": "Applying Operations (Operator Identification)",
            "ans": "b",
            "opts": ["Sequence A", "Sequence B", "Sequence C", "Sequence D"],
            "img": "nv3_q28.png"
        }
    ]

    for i, q_data in enumerate(questions_data):
        # Format options as JSON
        options_json = [{'id': chr(97 + j), 'text': opt} for j, opt in enumerate(q_data["opts"])]
        
        question = Question.objects.create(
            test=test,
            question_text=q_data["text"],
            question_type='mcq',
            options=options_json,
            correct_answer=q_data["ans"],
            difficulty_level='hard',
            order=i + 1
        )
        
        # Add Image
        image_name = q_data["img"]
        image_path = os.path.join(BASE_DIR, 'media/questions/images', image_name)
        
        if os.path.exists(image_path):
            with open(image_path, 'rb') as f:
                QuestionImage.objects.create(
                    question=question,
                    image=File(f, name=image_name),
                    caption=f"Visual reasoning for Question {i+1}",
                    order=0
                )
            print(f"🖼️ Question {i+1} created with image.")
        else:
            print(f"⚠️ Image NOT FOUND for Q{i+1}: {image_path}")

    # Finalize test stats
    test.total_questions = test.questions.count()
    test.save()
    print(f"\n✅ SUCCESS: Seeded {test.total_questions} questions for '{test_name}'")

if __name__ == "__main__":
    seed_nv_set3()
