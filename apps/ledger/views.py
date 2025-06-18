from rest_framework import viewsets
from .serializers import CategorySerializer, BudgetTypeSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Category, BudgetType
from ..utils.token import JWTAuthentication

class TypesViewSet(viewsets.ModelViewSet):
    queryset = BudgetType.objects.all()
    serializer_class = BudgetTypeSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        user = self.request.user
        return BudgetType.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
