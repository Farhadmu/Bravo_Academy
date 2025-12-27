from rest_framework import serializers
from .models import Question, QuestionImage

class QuestionImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionImage
        fields = ['id', 'image', 'caption', 'order']

class TestQuestionSerializer(serializers.ModelSerializer):
    """Minimal serializer for test-taking - excludes test field to reduce payload size"""
    class Meta:
        model = Question
        fields = ['id', 'question_text', 'question_type', 'options', 'order']

class QuestionSerializer(serializers.ModelSerializer):
    images = QuestionImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Question
        fields = ['id', 'test', 'question_text', 'question_type', 'options', 'difficulty_level', 'images']
        # Note: Excluding correct_answer and explanation from standard serializer to prevent cheating
        # Admin serializer would include them

class AdminQuestionSerializer(serializers.ModelSerializer):
    images = QuestionImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Question
        fields = '__all__'
