from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from .models import Tasks
from .forms import TaskForm


class TasksView(ListView):
    model = Tasks
    template_name = 'tasks/tasks_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Tasks.objects.all()


class TaskDetailView(DetailView):
    model = Tasks
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'


class CreateTask(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Tasks
    form_class = TaskForm
    template_name = 'tasks/task_create.html'
    success_url = reverse_lazy('tasks')
    success_message = 'Задача успешно создана'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdateTask(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Tasks
    form_class = TaskForm
    template_name = 'tasks/task_update.html'
    success_url = reverse_lazy('tasks')
    success_message = 'Задача успешно изменена'

    def test_func(self):
        return self.request.user == self.get_object().author

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, 'Вы не можете редактировать чужую задачу.')
            return redirect('tasks')
        else:
            messages.error(self.request, 'Вы не авторизованы')
            return redirect('login')

class DeleteTask(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Tasks
    template_name = 'tasks/task_delete.html'
    success_url = reverse_lazy('tasks')
    success_message = 'Задача успешно удалена'

    def test_func(self):
        return self.request.user == self.get_object().author

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, 'Вы не можете удалять чужую задачу.')
            return redirect('tasks')
        else:
            messages.error(self.request, 'Вы не авторизованы')
            return redirect('login')


