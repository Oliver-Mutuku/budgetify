from rest_framework import serializers
from django.utils.text import slugify
from .models import Category, Expense, Income, BudgetType


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'name', 'is_default']
        read_only_fields = ['id', 'slug', 'is_default']

    def validate_name(self, value):
        """
        Validate that the name does not cause a slug collision for this user.
        """
        request = self.context.get("request")
        user = request.user if request else None
        base_slug = slugify(value)
        instance = self.instance

        queryset = Category.objects.filter(slug=base_slug, user=user)
        if instance:
            queryset = queryset.exclude(id=instance.id)

        if queryset.exists():
            raise serializers.ValidationError(
                "A category with a similar name already exists for this user."
            )
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        name = validated_data['name']
        slug = slugify(name)

        validated_data['slug'] = slug
        validated_data['user'] = user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        Update the category and regenerate the slug if the name changes.
        """
        name = validated_data.get('name', instance.name)
        instance.slug = slugify(name)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

    def update(self, instance, validated_data):
        """
        update the category, regenerating the slug, if the category name changes
        """
        name = validated_data.get('name', instance.name)
        instance.slug = slugify(name)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


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
        read_only_fields = ("slug", "user")

    def validate_name(self, value):
        """
        Ensure that the slug generated from name is unique per user.
        """
        request = self.context.get("request")
        user = request.user if request else None
        base_slug = slugify(value)
        instance = self.instance

        # Check if another BudgetType with the same slug exists for this user
        queryset = BudgetType.objects.filter(slug=base_slug, user=user)
        if instance:
            queryset = queryset.exclude(id=instance.id)
        if queryset.exists():
            raise serializers.ValidationError(
                "A budget type with a similar name already exists for this user."
            )
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        name = validated_data['name']
        slug = slugify(name)

        validated_data['slug'] = slug
        validated_data['user'] = user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        name = validated_data.get("name", instance.name)
        instance.slug = slugify(name)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

