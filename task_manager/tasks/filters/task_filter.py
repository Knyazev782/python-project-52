from django_filters import FilterSet, ModelChoiceFilter, BooleanFilter, ModelMultipleChoiceFilter
from task_manager.tasks.models import Tasks
from task_manager.users.models import Users
from task_manager.statuses.models import Statuses
from task_manager.labels.models import Labels


class TaskFilter(FilterSet):
    status = ModelChoiceFilter(queryset=Statuses.objects.all())
    assigned_to = ModelChoiceFilter(queryset=Users.objects.all())
    labels = ModelMultipleChoiceFilter(queryset=Labels.objects.all())
    author = ModelChoiceFilter(queryset=Users.objects.all())
    self_tasks = BooleanFilter(
        field_name='author',
        method='filter_self_tasks',
        label='Только свои задачи'
    )

    class Meta:
        model = Tasks
        fields = ['status', 'assigned_to', 'labels', 'author']

    def filter_self_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset
