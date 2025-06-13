from rest_framework import serializers
from django.utils.text import slugify
from .models import Category, Expense, Income, BudgetType


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'name', "is_default"]
        read_only_fields = ['id', 'slug', "is_default"]

    def validate_name(self, value):
        """
        validate that the name doesn't result in a duplicate slug
        """
        base_slug = slugify(value)
        instance = self.instance

        # check for slug conflict , excluding the current instance during updates
        if Category.objects.filter(slug=base_slug).exclude(id=getattr(instance, 'id', None)).exists():
            raise serializers.ValidationError("A category with a similar name already exists. Please choose a different name")
        return value

    def create(self, validated_data):
        """
        create a new category with a generated name
        """
        name = validated_data['name']
        validated_data['slug'] = slugify(name)
        return super().create(validated_data)

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

    def validate_name(self, value):
        """
        validate that the name doesn't result in a duplicate slug
        """
        base_slug = slugify(value)
        instance = self.instance

        # check for slug conflict , excluding the current instance during updates
        if Category.objects.filter(slug=base_slug).exclude(id=getattr(instance, 'id', None)).exists():
            raise serializers.ValidationError(
                "A Budget Type with a similar name already exists. Please choose a different name")
        return value

    def create(self, validated_data):
        """
        create a new category with a generated name
        """
        name = validated_data['name']
        validated_data['slug'] = slugify(name)
        return super().create(validated_data)

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

