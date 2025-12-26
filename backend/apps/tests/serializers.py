from rest_framework import serializers
from .models import Test, TestSession

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['id', 'name', 'description', 'duration_minutes', 'total_questions', 'is_free', 'is_free_sample', 'price', 'created_at']

class TestSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestSession
        fields = ['id', 'test', 'user', 'started_at', 'submitted_at', 'status', 'score', 'percentage', 'passed', 'answers', 'time_limit_seconds']
        read_only_fields = ['user', 'started_at', 'submitted_at', 'score', 'percentage', 'passed', 'status', 'time_limit_seconds']

class PublicQuestionSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    question_text = serializers.CharField()
    options = serializers.JSONField()
    order = serializers.IntegerField()

class PublicEvaluationSerializer(serializers.Serializer):
    score = serializers.IntegerField()
    total = serializers.IntegerField()
    percentage = serializers.FloatField()
    accuracy = serializers.FloatField()
    review = serializers.ListField(child=serializers.DictField())
