from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

urlpatterns = [
    path("", views.listing_list, name="listing-list"),
    path("pretraga", views.ListingSearchView.as_view(), name="listing-search"),
    path("<int:pk>", views.ListingDetailView.as_view(), name="listing-detail"),
    
    # 4 Authentication & authorization
    path("postavka", login_required(views.listing_create), name="listing-create"),
    path("<int:pk>/izmena", login_required(views.ListingUpdateView.as_view()), name="listing-edit"),
    path("<int:pk>/brisanje", login_required(views.listing_delete), name="listing-delete"),
    path("<int:pk>/cuvanje", login_required(views.listing_save), name="listing-save"),
]
