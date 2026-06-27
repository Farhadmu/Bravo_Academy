import re
from django.conf import settings
from rest_framework import serializers
from .models import Question, QuestionImage

class QuestionImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionImage
        fields = ['id', 'image', 'caption', 'order']

    def _get_supabase_public_url(self):
        """Dynamically derive Supabase public bucket URL from Django settings."""
        endpoint = getattr(settings, 'AWS_S3_ENDPOINT_URL', '')
        bucket = getattr(settings, 'AWS_STORAGE_BUCKET_NAME', 'media')
        match = re.search(r'https?://([^.]+)\.storage\.supabase\.co', endpoint)
        if match:
            project_id = match.group(1)
            return f"https://{project_id}.supabase.co/storage/v1/object/public/{bucket}"
        return None

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.image:
            url = ret['image']
            # If S3 storage is configured and returned a proper URL, use it as-is
            if url and ('://' in url):
                return ret
            # Fallback: construct Supabase public URL from stored path
            supabase_url = self._get_supabase_public_url()
            if supabase_url:
                ret['image'] = f"{supabase_url}/{instance.image.name}"
        return ret

class TestQuestionSerializer(serializers.ModelSerializer):
    """Minimal serializer for test-taking - excludes test field to reduce payload size"""
    images = QuestionImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Question
        fields = ['id', 'question_text', 'question_type', 'options', 'order', 'images']

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
