from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import ProtectedError
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from .models import Statuses
from .forms import StatusForm


class StatusesView(ListView):
    model = Statuses
    template_name = 'statuses/statuses_list.html'
    context_object_name = 'statuses'

    def get_queryset(self):
        return Statuses.objects.all()


class CreateStatus(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Statuses
    form_class = StatusForm
    template_name = 'statuses/create_status.html'
    success_url = reverse_lazy('statuses')
    success_message = 'Статус успешно создан'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class UpdateStatus(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Statuses
    form_class = StatusForm
    template_name = 'statuses/update_status.html'
    success_url = reverse_lazy('statuses')
    success_message = 'Статус успешно изменён'

    def test_func(self):
        return self.request.user == self.get_object().created_by

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, 'Вы не можете редактировать чужой статус.')
        else:
            messages.error(self.request, 'Вы не авторизованы')
        return redirect(self.success_url if self.request.user.is_authenticated else 'login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response


class DeleteStatus(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Statuses
    template_name = 'statuses/delete_status.html'
    success_url = reverse_lazy('statuses')

    def test_func(self):
        return self.request.user == self.get_object().created_by

    def handle_no_permission(self):
        messages.error(self.request, 'Вы не можете удалить чужой статус.')
        return redirect(self.success_url)

    def form_valid(self, form):
        try:
            self.object.delete()
            messages.success(self.request, 'Статус успешно удалён')
            return redirect(self.success_url)
        except ProtectedError:
            messages.error(self.request, 'Нельзя удалить статус, потому что он используется')
            return redirect(self.success_url)
