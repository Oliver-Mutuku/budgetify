from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from .serializers import CategorySerializer, BudgetTypeSerializer, IncomeSerializer, ExpenseSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Category, BudgetType, Income, Expense
from ..utils.token import JWTAuthentication
from .filters import ExpenseFilter, IncomeFilter
from rest_framework.filters import SearchFilter


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


class IncomeViewSet(viewsets.ModelViewSet):
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = IncomeFilter
    search_fields = ['source', 'description']

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication, SearchFilter]

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ExpenseFilter
    search_fields = ['title', 'category__name', 'budget_type__name', 'description']

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
