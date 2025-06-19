from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, TypesViewSet, ExpenseViewSet, IncomeViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'types', TypesViewSet, basename='budget_type')
router.register(r'incomes', IncomeViewSet, basename='income')
router.register(r'expenses', ExpenseViewSet, basename='expense')
urlpatterns =router.urls