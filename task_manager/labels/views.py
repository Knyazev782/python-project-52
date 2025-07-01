from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import ProtectedError
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from .models import Labels
from .forms import LabelForm


class LabelsView(ListView):
    model = Labels
    template_name = 'labels/label_list.html'
    context_object_name = 'labels'

    def get_queryset(self):
        return Labels.objects.all()


class CreateLabel(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Labels
    form_class = LabelForm
    template_name = 'labels/label_create.html'
    success_url = reverse_lazy('labels')
    success_message = 'Метка успешно создана'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class UpdateLabel(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Labels
    form_class = LabelForm
    template_name = 'labels/label_update.html'
    success_url = reverse_lazy('labels')
    success_message = 'Метка успешно изменена'

    def test_func(self):
        return self.request.user == self.get_object().created_by

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, 'Вы не можете редактировать чужую метку.')
            return redirect('labels')
        return redirect('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response


class DeleteLabel(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Labels
    success_url = reverse_lazy('labels')
    template_name = 'labels/label_delete.html'
    permission_denied_message = 'Вы не можете удалить чужую метку.'

    def test_func(self):
        label = self.get_object()
        return self.request.user == label.created_by

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return redirect(self.success_url)

    def form_valid(self, form):
        try:
            self.object.delete()
            messages.success(self.request, 'Метка успешно удалена')
            return redirect('labels')
        except ProtectedError:
            messages.error(self.request, 'Нельзя удалить метку, потому что она используется')
            return redirect('labels')
