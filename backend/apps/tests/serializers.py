from rest_framework import serializers
from .models import Test, TestSession

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['id', 'name', 'description', 'duration_minutes', 'total_questions', 'is_free', 'is_free_sample', 'is_bank', 'price', 'created_at']

class TestSessionSerializer(serializers.ModelSerializer):
    remaining_seconds = serializers.SerializerMethodField()

    class Meta:
        model = TestSession
        fields = ['id', 'test', 'user', 'started_at', 'submitted_at', 'status', 'score', 'percentage', 'passed', 'answers', 'time_limit_seconds', 'remaining_seconds']
        read_only_fields = ['user', 'started_at', 'submitted_at', 'score', 'percentage', 'passed', 'status', 'time_limit_seconds', 'remaining_seconds']

    def get_remaining_seconds(self, obj):
        if obj.status != 'in_progress':
            return 0
        from django.utils import timezone
        now = timezone.now()
        elapsed = (now - obj.started_at).total_seconds()
        remaining = obj.time_limit_seconds - elapsed
        return max(0, int(remaining))

class PublicQuestionSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    question_text = serializers.CharField()
    options = serializers.JSONField()
    order = serializers.IntegerField()
    images = serializers.SerializerMethodField()

    def get_images(self, obj):
        from apps.questions.serializers import QuestionImageSerializer
        return QuestionImageSerializer(obj.images.all(), many=True, context=self.context).data

class PublicEvaluationSerializer(serializers.Serializer):
    score = serializers.IntegerField()
    total = serializers.IntegerField()
    percentage = serializers.FloatField()
    accuracy = serializers.FloatField()
    review = serializers.ListField(child=serializers.DictField())
