from rest_framework import serializers
from .models import Category, Expense, Income, BudgetType


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

    def validate(self, attrs):
        user = self.context['request'].user
        name = attrs.get('name')

        if self.instance is None:
            if Category.objects.filter(name=name, user=user).exists():
                raise serializers.ValidationError({
                    "name": "You already have a category with this name."
                })
        else:
            if Category.objects.filter(name=name, user=user).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError({
                    "name": "You already have a category with this name."
                })
        return attrs

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)



class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = "__all__"


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = "__all__"


class BudgetTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetType
        fields = "__all__"

    def validate(self, attrs):
        user = self.context['request'].user
        name = attrs.get('name')

        if self.instance is None:
            if Category.objects.filter(name=name, user=user).exists():
                raise serializers.ValidationError({
                    "name": "You already have a budget type with this name."
                })
        else:
            if Category.objects.filter(name=name, user=user).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError({
                    "name": "You already have a budget type with this name."
                })
        return attrs

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
