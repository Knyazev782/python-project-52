from django.shortcuts import redirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Tasks
from .forms import TaskForm


class TasksView(ListView):
    model = Tasks
    template_name = 'tasks/task_list.html'


class CreateTask(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Tasks
    form_class = TaskForm
    template_name = 'tasks/task_create.html'
    success_url = reverse_lazy('tasks')
    success_message = 'Задача успешно создана'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


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
