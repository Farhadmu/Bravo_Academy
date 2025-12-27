from rest_framework import viewsets, permissions
from .models import Question
from .serializers import QuestionSerializer, AdminQuestionSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get_serializer_class(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return AdminQuestionSerializer
        return QuestionSerializer

    def get_queryset(self):
        # Optimize query with select_related to prevent N+1 queries
        # Use only() to fetch minimal fields for better performance
        queryset = Question.objects.select_related('test').only(
            'id', 'test_id', 'question_text', 'question_type', 
            'options', 'difficulty_level', 'order', 'bank_order'
        )
        
        test_id = self.request.query_params.get('test_id', None)
        
        if test_id is not None:
            queryset = queryset.filter(test_id=test_id)
        
        return queryset.order_by('bank_order', 'order', 'created_at')
