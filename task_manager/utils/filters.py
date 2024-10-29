import django_filters
from django import forms
from django.utils.translation import gettext_lazy as _
from ..tasks.models import Task
from ..labels.models import Label


class TaskFilter(django_filters.FilterSet):

    label = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        label=_('Label'),
        field_name="labels",
        widget=forms.Select(attrs={'class': 'form-select mr-3 ml-2'})
    )

    self_tasks = django_filters.BooleanFilter(
        method='filter_self_tasks',
        label=_('Only own tasks'),
        widget=forms.CheckboxInput,
        required=False
    )

    def filter_self_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset

    class Meta:
        model = Task
        fields = ['status', 'executor']
