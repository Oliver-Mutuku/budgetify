from rest_framework import serializers
from .models import Category, Expense, Income, BudgetType


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'name']
        read_only_fields = ['id', 'slug']

    def update(self, instance, validated_data):
        print(validated_data)
        return


