from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from .models import Users
from .forms import UserRegistrationForm, UserLoginForm

class UsersView(ListView):
    model = Users
    template_name = 'users/user_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        return Users.objects.all()

class CreateUser(SuccessMessageMixin, CreateView):
    model = Users
    form_class = UserRegistrationForm
    template_name = 'users/user_create.html'
    success_url = reverse_lazy('login')
    success_message = 'Пользователь успешно зарегистрирован'

class UpdateUser(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Users
    form_class = UserRegistrationForm
    template_name = 'users/user_update.html'
    success_url = reverse_lazy('users')
    success_message = 'Пользователь успешно изменён'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object != request.user:
            messages.error(request, 'Вы не можете редактировать других пользователей')
            return redirect('users')
        return super().dispatch(request, *args, **kwargs)

class DeleteUser(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Users
    template_name = 'users/user_delete.html'
    success_url = reverse_lazy('users')
    success_message = 'Пользователь успешно удалён'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object != request.user:
            messages.error(request, 'Вы не можете удалять других пользователей')
            return redirect('users')
        return super().dispatch(request, *args, **kwargs)

def login_view(request):
    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Вы успешно вошли в систему.')
            return redirect('index')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')
    else:
        form = UserLoginForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы.')
    return redirect('login')