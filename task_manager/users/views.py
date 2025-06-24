from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.db.models import ProtectedError
from .models import Users
from .forms import UserRegistrationForm
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.http import HttpResponseRedirect

class UsersView(ListView):
    model = Users
    template_name = 'users/user_list.html'

    def get_queryset(self):
        return Users.objects.all()

class CreateUser(SuccessMessageMixin, CreateView):
    model = Users
    form_class = UserRegistrationForm
    template_name = 'users/user_create.html'
    success_url = reverse_lazy('login')
    success_message = "Пользователь успешно зарегистрирован."

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class UpdateUser(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Users
    form_class = UserRegistrationForm
    template_name = 'users/user_update.html'
    success_url = reverse_lazy('users')
    success_message = "Пользователь успешно изменен."

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object != request.user:
            messages.error(request, "Вы можете изменять только себя.")
            return redirect('users')
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return super().get_object(queryset)

class DeleteUser(LoginRequiredMixin, DeleteView):
    model = Users
    template_name = 'users/user_delete.html'
    success_url = reverse_lazy('users')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object != request.user:
            messages.error(request, "Вы можете удалять только себя.")
            return redirect('users')
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return super().get_object(queryset)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            messages.success(request, "Пользователь успешно удален.")
        except ProtectedError:
            messages.error(request, "Нельзя удалить пользователя, так как он связан с задачами.")
        return redirect(self.success_url)

class CustomLoginView(auth_views.LoginView):
    template_name = 'registration/login.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Вы залогинены")
        return response

class CustomLogoutView(auth_views.LogoutView):
    template_name = 'registration/logout.html'
    next_page = '/'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout = super().post(request, *args, **kwargs)
        return HttpResponseRedirect(self.next_page)