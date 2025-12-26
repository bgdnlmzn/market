from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView

from .forms import LoginForm, SignUpForm


class SignUpView(FormView):
    template_name = "accounts/signup.html"
    form_class = SignUpForm
    success_url = reverse_lazy("catalog:equipment_list")

    def form_valid(self, form: SignUpForm):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Добро пожаловать! Аккаунт создан.")
        return super().form_valid(form)


class SignInView(LoginView):
    template_name = "accounts/login.html"
    form_class = LoginForm

    def form_valid(self, form):
        messages.success(self.request, "С возвращением!")
        return super().form_valid(form)


class SignOutView(LogoutView):
    next_page = reverse_lazy("catalog:equipment_list")

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, "Вы вышли из аккаунта.")
        return super().dispatch(request, *args, **kwargs)

    def get_next_page(self):
        # Всегда уходим на главную страницу каталога
        return reverse_lazy("catalog:equipment_list")


def logout_view(request):
    logout(request)
    messages.info(request, "Вы вышли из аккаунта.")
    return redirect(reverse("catalog:equipment_list"))


@login_required
def profile(request):
    return render(request, "accounts/profile.html")
