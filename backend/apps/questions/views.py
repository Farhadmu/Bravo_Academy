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
        queryset = Question.objects.all()
        test_id = self.request.query_params.get('test_id', None)
        set_number = self.request.query_params.get('set_number', None)
        
        if test_id is not None:
            from apps.tests.models import Test
            try:
                test = Test.objects.get(id=test_id)
                if test.is_bank and set_number:
                    set_num = int(set_number)
                    start_range = (set_num - 1) * 100 + 1
                    end_range = set_num * 100
                    queryset = queryset.filter(test=test, bank_order__gte=start_range, bank_order__lte=end_range)
                else:
                    queryset = queryset.filter(test=test)
            except Test.DoesNotExist:
                queryset = queryset.filter(test_id=test_id)
        
        return queryset.order_by('bank_order', 'order', 'created_at')
