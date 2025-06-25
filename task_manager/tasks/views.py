from django.shortcuts import redirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django_filters.views import FilterView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Tasks
from .forms import TaskForm
from .filters.task_filter import TaskFilter


class TasksView(FilterView, ListView):
    model = Tasks
    filterset_class = TaskFilter
    template_name = 'tasks/tasks_list.html'


class CreateTask(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Tasks
    form_class = TaskForm
    template_name = 'tasks/task_create.html'
    success_url = reverse_lazy('tasks')
    success_message = 'Задача успешно создана'

    def form_valid(self, form):
        form.instance.author = self.request.user
        if not form.cleaned_data.get('status'):
            from task_manager.statuses.models import Statuses
            default_status = Statuses.objects.first()  # Берем первый доступный статус
            if default_status:
                form.instance.status = default_status
        if not form.cleaned_data.get('assigned_to'):
            from task_manager.users.models import Users
            default_user = Users.objects.first()  # Берем первого доступного пользователя
            if default_user:
                form.instance.assigned_to = default_user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from task_manager.statuses.models import Statuses
        from task_manager.users.models import Users
        if not Statuses.objects.exists():
            messages.error(self.request, 'Нет доступных статусов для выбора.')
        if not Users.objects.exists():
            messages.error(self.request, 'Нет доступных пользователей для назначения.')
        return context


class UpdateTask(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Tasks
    form_class = TaskForm
    template_name = 'tasks/task_update.html'
    success_url = reverse_lazy('tasks')
    success_message = 'Задача успешно обновлена'

    def dispatch(self, request, *args, **kwargs):
        task = self.get_object()
        if task.author != self.request.user:
            messages.error(request, 'Вы не можете изменять эту задачу!')
            return redirect('tasks')
        return super().dispatch(request, *args, **kwargs)


class DeleteTask(LoginRequiredMixin, DeleteView):
    model = Tasks
    template_name = 'tasks/task_delete.html'
    success_url = reverse_lazy('tasks')
    success_message = 'Задача успешно удалена'

    def dispatch(self, request, *args, **kwargs):
        task = self.get_object()
        if task.author != self.request.user:
            messages.error(request, 'Вы не можете удалять эту задачу!')
            return redirect('tasks')
        return super().dispatch(request, *args, **kwargs)


class DetailTask(LoginRequiredMixin, DetailView):
    model = Tasks
    template_name = 'tasks/task_detail.html'
