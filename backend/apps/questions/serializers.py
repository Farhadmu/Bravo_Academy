from rest_framework import serializers
from .models import Question, QuestionImage

class QuestionImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionImage
        fields = ['id', 'image', 'caption', 'order']

    def to_representation(self, instance):
        """
        Emergency Fix: Ensure Supabase URLs are used even if storage backend fails.
        """
        ret = super().to_representation(instance)
        if instance.image:
            url = ret['image']
            # If URL is pointing to Render's local media but should be Supabase
            if '/media/questions/' in url and 'supabase.co' not in url:
                # Construct the correct public URL
                # Hardcoded foundation based on confirmed Supabase config
                supabase_domain = "https://jjxusciiuvcjltkreozq.supabase.co/storage/v1/object/public/media"
                # Extract relative path from /media/
                relative_path = url.split('/media/')[-1]
                ret['image'] = f"{supabase_domain}/{relative_path}"
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
