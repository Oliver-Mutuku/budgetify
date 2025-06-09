from rest_framework import viewsets
from .serializers import CategorySerializer
from rest_framework.permissions import AllowAny
from .models import Category


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny]
