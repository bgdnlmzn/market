from django.urls import path

from .views import SignInView, SignOutView, SignUpView, logout_view, profile

app_name = "accounts"

urlpatterns = [
    path("login/", SignInView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("profile/", profile, name="profile"),
]

