from rest_framework import serializers
from .models import Result, PerformanceAnalytics

class ResultSerializer(serializers.ModelSerializer):
    test_name = serializers.ReadOnlyField(source='test.name')
    
    class Meta:
        model = Result
        fields = [
            'id', 'test', 'test_name', 'test_session', 
            'total_questions', 'correct_answers', 'wrong_answers', 'unanswered',
            'score_percentage', 'passed', 'time_taken_seconds', 'accuracy', 'created_at'
        ]

class ResultDetailSerializer(ResultSerializer):
    review_data = serializers.SerializerMethodField()

    class Meta(ResultSerializer.Meta):
        fields = ResultSerializer.Meta.fields + ['review_data']

    def get_review_data(self, obj):
        from apps.questions.models import Question
        
        session = obj.test_session
        user_answers = session.answers or {}
        
        questions = Question.objects.filter(test=obj.test).order_by('bank_order', 'order', 'created_at')
        
        review = []
        for q in questions:
            user_answer = user_answers.get(str(q.id))
            review.append({
                'id': q.id,
                'question_text': q.question_text,
                'options': q.options,
                'correct_answer': q.correct_answer,
                'user_answer': user_answer,
                'explanation': q.explanation,
                'is_correct': str(q.correct_answer) == str(user_answer) if user_answer is not None else False
            })
        return review

class PerformanceAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceAnalytics
        fields = [
            'id', 'total_tests_taken', 'total_tests_passed',
            'average_score', 'average_accuracy', 'highest_score', 'lowest_score',
            'average_time_taken', 'total_time_spent', 'average_questions_answered',
            'updated_at'
        ]
