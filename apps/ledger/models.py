from django.db import models
from django.conf import settings
from django.utils.text import slugify # to turn any string into a slugified string


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'category'
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Expense(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='expenses')
    title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    budget_type = models.ForeignKey('BudgetType', on_delete=models.SET_NULL, null=True, to_field='slug', related_name='expenses')
    description = models.TextField(blank=True)
    date = models.DateField() # for filtering purposes
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']
        db_table = 'expense'

    def __str__(self):
        return f"{self.title} - ksh{self.amount} on {self.date}"
    

class Income(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="incomes")
    source = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']
        db_table = 'income'

    def __str__(self):
        return f"{self.source} - ksh{self.amount} on {self.date}"


class BudgetType(models.Model):
    slug = models.SlugField(primary_key=True, unique=True, max_length=50, blank=True)
    name = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='budget_types')
    description = models.TextField(blank=True)


    class Meta:
        unique_together = ('user', 'name')
        verbose_name = 'budget type'
        verbose_name_plural = 'budget types'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.slug})"


