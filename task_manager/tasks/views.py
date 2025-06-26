from django.shortcuts import redirect, reverse, render
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django_filters.views import FilterView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
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

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.instance.author = self.request.user
            form.save()
            messages.success(request, self.success_message)
            return HttpResponseRedirect(reverse('tasks'))
        return render(request, self.template_name, {'form': form})


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
