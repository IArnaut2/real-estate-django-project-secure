from django.urls import path

from . import views

# 4 Authentication & authorization
urlpatterns = [
  path("registracija", views.register, name="register"),
  path("prijava", views.login2, name="login"),
  path("odjava", views.logout2, name="logout")
]