from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from task_manager.labels.models import Labels
from task_manager.labels.forms import LabelsForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages


class LabelsView(LoginRequiredMixin, ListView):
    model = Labels
    template_name = 'labels/label_list.html'

class CreateLabels(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Labels
    form_class = LabelsForm
    template_name = 'labels/label_create.html'
    success_url = reverse_lazy('labels')
    success_message = 'Метка успешно создана'

class UpdateLabels(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Labels
    form_class = LabelsForm
    template_name = 'labels/label_update.html'
    success_url = reverse_lazy('labels')
    success_message = 'Метка обновлена'

class DeleteLabels(LoginRequiredMixin, DeleteView):
    model = Labels
    template_name = 'labels/label_delete.html'
    success_url = reverse_lazy('labels')
    success_message = "Метка успешно удалена"

    def dispatch(self, request, *args, **kwargs):
        label = self.get_object()
        if label.tasks.exists():
            messages.error(request, 'Нельзя удалить метку, связанную с задачами')
            return redirect('labels')
        return super().dispatch(request, *args, **kwargs)
