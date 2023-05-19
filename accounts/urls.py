from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("register/business/", views.register_business, name="register_business"),
    path("update/business/", views.update_business, name="update_business"),
    path("register/user/", views.register_user, name="register_user"),
    path("update/user/", views.update_user, name="update_user"),
    path("profile/", views.user_profile, name="user_profile"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]
