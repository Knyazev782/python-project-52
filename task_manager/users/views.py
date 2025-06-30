from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .models import Users
from .forms import UserRegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import ProtectedError

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

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            messages.success(request, 'Пользователь успешно удалён')
            return redirect(self.success_url)
        except ProtectedError:
            messages.error(request, 'Нельзя удалить пользователя, потому что он используется')
            return redirect(self.success_url)


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Неверное имя пользователя или пароль.")
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})