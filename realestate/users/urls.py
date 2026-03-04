from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

urlpatterns = [
    path("<int:pk>", views.detail, name="user-detail"),
    
    # 4 Authentication & authorization
    path("profil", login_required(views.detail), name="my-profile"),
    path("sacuvani", login_required(views.saved), name="user-saved"),
    path("podesavanja", login_required(views.settings), name="user-settings"),
    path("izmena", login_required(views.update), name="user-update"),
    path("izmena2", login_required(views.update2), name="user-update2"),
    path("brisanje", login_required(views.delete), name="user-delete"),
]
