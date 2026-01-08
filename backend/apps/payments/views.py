from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Payment, UserTestAccess
from .serializers import PaymentSerializer, UserTestAccessSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'head', 'options']

    def get_queryset(self):
        if self.request.user.is_staff:
            return Payment.objects.all()
        return Payment.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def verify(self, request, pk=None):
        payment = self.get_object()
        notes = request.data.get('notes', '')
        payment.mark_as_verified(request.user, notes)
        
        # Grant access
        UserTestAccess.objects.get_or_create(
            user=payment.user,
            test=payment.test,
            defaults={'payment': payment, 'granted_by': request.user}
        )
        
        return Response({'status': 'verified'})

class UserTestAccessViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserTestAccess.objects.all()
    serializer_class = UserTestAccessSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserTestAccess.objects.filter(user=self.request.user, is_active=True)
