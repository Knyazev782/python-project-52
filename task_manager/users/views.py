from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Users
from .forms import RegistrationUserForm, UpdateUserForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages


def index(request):
    return render(request, 'index.html')


class UserListView(ListView):
    model = Users
    template_name = 'user_list.html'


class CreateUserView(CreateView):
    model = Users
    form_class = RegistrationUserForm
    success_url = '/login/'
    template_name = 'create_users.html'
    def form_valid(self, form):
        messages.success(self.request, 'Пользователь успешно создан')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка при регистрации')
        return super().form_invalid(form)


class UpdateUserView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Users
    form_class = UpdateUserForm
    success_url = '/users/'
    template_name = 'update_users.html'

    def test_func(self):
        return self.request.user == self.get_object()


    def handle_no_permission(self):
        messages.error(self.request, 'Вам нельзя редактировать этого пользователя')
        return super().handle_no_permission()



class DeleteUserView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Users
    success_url = '/users/'
    template_name = 'delete_users.html'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Пользователь успешно удалён')
        return super().delete(request, *args, **kwargs)

    def test_func(self):
        return self.request.user == self.get_object()

    def handle_no_permission(self):
        messages.error(self.request, 'Вам нельзя удалять этого пользователя')
        return super().handle_no_permission()