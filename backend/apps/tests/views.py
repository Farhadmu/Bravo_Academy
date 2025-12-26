from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Test, TestSession
from .serializers import TestSerializer, TestSessionSerializer

class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Test.objects.filter(is_active=True)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def start_session(self, request, pk=None):
        test = self.get_object()
        # Check for active session
        active_session = TestSession.objects.filter(user=request.user, test=test, status='in_progress').first()
        if active_session:
            return Response(TestSessionSerializer(active_session).data)

        session = TestSession.objects.create(
            user=request.user,
            test=test,
            time_limit_seconds=test.duration_minutes * 60,
            status='in_progress'
        )
        return Response(TestSessionSerializer(session).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def get_sample_test(self, request):
        """Get the current active free sample test."""
        test = Test.objects.filter(is_free_sample=True, is_active=True).first()
        if not test:
            # Fallback to Set 1 if no is_free_sample flag is found
            test = Test.objects.filter(name__icontains="Set 1").first()
        
        if not test:
            return Response({"error": "No sample test found"}, status=status.HTTP_404_NOT_FOUND)
            
        return Response(TestSerializer(test).data)

    @action(detail=True, methods=['get'], permission_classes=[permissions.AllowAny])
    def public_questions(self, request, pk=None):
        """Get questions for a public sample test (Set 1)."""
        test = self.get_object()
        # For public access, we might restrict this only to specific tests (e.g., Set 1)
        # But for now, we allow any test to be taken publicly if the ID is known. 
        # Ideally, check test.is_free_sample or similar.
        
        from apps.questions.models import Question
        from .serializers import PublicQuestionSerializer
        
        questions = Question.objects.filter(test=test).order_by('order')
        return Response(PublicQuestionSerializer(questions, many=True).data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.AllowAny])
    def public_evaluate(self, request, pk=None):
        """Evaluate answers for a public sample test."""
        test = self.get_object()
        user_answers = request.data.get('answers', {})
        
        from apps.questions.models import Question
        from .serializers import PublicEvaluationSerializer
        
        questions = Question.objects.filter(test=test).order_by('order')
        
        score = 0
        total = questions.count()
        answered_count = 0
        review_data = []
        
        for q in questions:
            user_ans_id = user_answers.get(str(q.id))
            is_correct = False
            
            if user_ans_id:
                answered_count += 1
                is_correct = str(q.correct_answer) == str(user_ans_id)
            
            if is_correct:
                score += 1
                
            review_data.append({
                'id': str(q.id),
                'question_text': q.question_text,
                'options': q.options,
                'correct_answer': q.correct_answer,
                'user_answer': user_ans_id,
                'explanation': q.explanation,
                'is_correct': is_correct
            })
            
        percentage = (score / total * 100) if total > 0 else 0
        accuracy = (score / answered_count * 100) if answered_count > 0 else 0
        
        return Response(PublicEvaluationSerializer({
            'score': score,
            'total': total,
            'percentage': percentage,
            'accuracy': accuracy,
            'review': review_data
        }).data)

class TestSessionViewSet(viewsets.ModelViewSet):
    queryset = TestSession.objects.all()
    serializer_class = TestSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TestSession.objects.filter(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        session = self.get_object()
        if session.status != 'in_progress':
            return Response({"error": "Test already submitted or expired"}, status=status.HTTP_400_BAD_REQUEST)
            
        # Optional: update answers one last time
        if 'answers' in request.data:
            session.answers = request.data['answers']

        session.submit_test() # This uses the model method we optimized
        return Response(TestSessionSerializer(session).data)
