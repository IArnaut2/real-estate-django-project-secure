from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpRequest
from django.shortcuts import  redirect, render

from .forms import UserUpdateForm, UserDeleteForm
from .repositories import user_repo

from listings.helpers.dropdowns import order_list
from listings.repositories import listing_repo

# Create your views here.
# Main
def detail(req: HttpRequest, pk):
    order = req.GET.get("redosled") if "redosled" in req.GET else ""
    page = req.GET.get("strana")

    user = user_repo.find_by_pk(pk)
    listings = listing_repo.find_by_user(user, order)
    paginator = Paginator(listings, per_page=2)
    listings = paginator.get_page(page)
    return render(req, "users/user_detail.html", {
        "user": user,
        "order_list": order_list,
        "listings": listings
    })

def update(req: HttpRequest):
    user = req.user
    update_form = UserUpdateForm(req.POST, instance=user)

    # 2 Input validation & sanitization
    if update_form.is_valid():
        if not user_repo.passwords_match(update_form.cleaned_data["curr_password"], user.password):
            messages.error(req, "Šifra je pogrešna. Pokušaj ponovo.")
            return redirect("user-update")
        
        if user_repo.passwords_match(update_form.cleaned_data["password"], user.password):
            messages.error(req, "Nova šifra ne sme biti ista prethodnoj. Pokušaj ponovo.")
            return redirect("user-update")
        
        user_repo.update(user, update_form.cleaned_data)
        return redirect("user-detail", kwargs={"id": user.id})


def delete(req: HttpRequest):
    user = req.user
    update_form = UserUpdateForm(instance=user)
    delete_form = UserDeleteForm(req.POST)

    # 2 Input validation & sanitization
    if delete_form.is_valid():
        if user_repo.passwords_match(delete_form.cleaned_data["password"], user.password):
            user_repo.delete(user)
            return redirect("logout")
        
        messages.error(req, "Šifra je pogrešna. Pokušaj ponovo.")
        return redirect("user-delete")

# Other
def saved(req: HttpRequest):
    user = req.user
    order = req.GET.get("redosled") if "redosled" in req.GET else ""
    page = req.GET.get("strana")

    listings = listing_repo.find_saved(user, order)
    paginator = Paginator(listings, per_page=3)
    listings = paginator.get_page(page)
    return render(req, "users/user_detail.html", {
        "user": user,
        "order_list": order_list,
        "listings": listings
    })

def settings(req: HttpRequest):
    pass

def update2(req: HttpRequest):
    pass