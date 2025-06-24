import django_filters
from .models import Expense, Income
from django.utils import timezone
from datetime import timedelta


class ExpenseFilter(django_filters.FilterSet):
    filter_by = django_filters.CharFilter(method='filter_by_date_range')
    start = django_filters.DateFilter(field_name='date_of_expense', lookup_expr='gte')
    end = django_filters.DateFilter(field_name='date_of_expense', lookup_expr='lte')

    class Meta:
        model = Expense
        fields = ['filter_by', 'start', 'end', 'category', 'budget_type']

    def filter_by_date_range(self, queryset, name, value):
        today = timezone.now().date()

        if value == 'past_week':
            start_date = today - timedelta(7)
        elif value == 'last_month':
            start_date = today - timedelta(30)
        elif value == 'last_3_months':
            start_date = today - timedelta(90)
        else:
            return queryset
        return queryset.filter(date_of_expense__gte=start_date)
