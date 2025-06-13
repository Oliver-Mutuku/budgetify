from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, TypesViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'types', TypesViewSet, basename='budget_type')
urlpatterns =router.urls