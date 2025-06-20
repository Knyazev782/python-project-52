from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.db.models import ProtectedError
from .models import Statuses
from .forms import CreateStatusForm
from django.contrib import messages
from django.http import HttpResponse
import rollbar

class StatusesView(ListView):
    model = Statuses
    template_name = 'statuses/statuses_list.html'

    def get_queryset(self):
        return Statuses.objects.all()

class CreateStatus(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Statuses
    form_class = CreateStatusForm
    template_name = 'statuses/create_status.html'
    success_url = reverse_lazy('statuses')
    success_message = "Статус успешно создан."

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class UpdateStatus(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Statuses
    form_class = CreateStatusForm
    template_name = 'statuses/update_status.html'
    success_url = reverse_lazy('statuses')
    success_message = "Статус успешно изменен."

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.created_by != request.user:
            messages.error(request, "Вы можете изменять только свои статусы.")
            return redirect('statuses')
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return super().get_object(queryset)

class DeleteStatus(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Statuses
    template_name = 'statuses/delete_status.html'
    success_url = reverse_lazy('statuses')
    success_message = "Статус успешно удален."

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.created_by != request.user:
            messages.error(request, "Вы можете удалять только свои статусы.")
            return redirect('statuses')
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return super().get_object(queryset)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            messages.success(request, self.success_message)
        except ProtectedError:
            messages.error(request, "Нельзя удалить статус, так как он используется.")
        return redirect(self.success_url)

def test_error_view(request):
    try:
        1 / 0  # Это вызовет деление на ноль
    except ZeroDivisionError:
        rollbar.report_exc_info()
    return HttpResponse("Ошибка отправлена в Rollbar!")