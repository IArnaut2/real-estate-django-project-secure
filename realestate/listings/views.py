from django.core.paginator import Paginator
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse

from realestate.globals import logger

from .forms import TermsForm, ListingForm
from .helpers.dropdowns import order_list
from .repositories import terms_repo, listing_repo

# Create your views here.
# Main
def listing_list(req: HttpRequest):
    username = f"{req.user}" if req.user.is_authenticated else "'guest'"
    order = req.GET.get("redosled") if "redosled" in req.GET else ""
    page = req.GET.get("strana")

    listings = listing_repo.find_all(order)
    paginator = Paginator(listings, per_page=2)
    listings = paginator.get_page(page)

    # 5 Security logging
    logger.info("User %s accessed: Listing list page.", username)
    return render(req, "listings/listing_list.html", {
        "order_list": order_list,
        "listings": listings
    })

def listing_create_get(req: HttpRequest, template: str):
    terms_form = TermsForm()
    listing_form = ListingForm()

    # 5 Security logging
    logger.info("User %s accessed: Listing create page.", f"{req.user}")
    return render(req, template, {
        "terms_form": terms_form,
        "listing_form": listing_form
    })

def listing_create_post(req: HttpRequest, template: str):
    terms_form = TermsForm(req.POST)
    listing_form = ListingForm(req.POST)
    forms = {
        "terms_form": terms_form,
        "listing_form": listing_form
    }
    
    # 2 Input validation & sanitization
    if not all([form.is_valid() for form in forms.values()]):
        # 5 Security logging
        logger.error("Listing posting failed due to validation errors.")
        return render(req, template, forms)

    items = listing_form.cleaned_data.pop("items")
    terms = terms_repo.find_or_create(terms_form.cleaned_data)
    poster = req.user
    listing_repo.create(items, terms, poster, listing_form.cleaned_data)

    # 5 Security logging
    logger.info("User %s posted a new listing.", f"{req.user}")
    return redirect(reverse("listing-list"))

def listing_create(req: HttpRequest):
    template = "listings/listing_create.html"
    return listing_create_post(req, template) if req.method == "POST" else listing_create_get(req, template)

def listing_update_get(req: HttpRequest, pk: int, template: str):
    listing = listing_repo.find_by_pk(pk)
    terms = listing.terms
    
    # 4 Authentication & authorization
    if req.user == listing.poster:
        terms_form = TermsForm(instance=terms)
        listing_form = ListingForm(instance=listing)
        return render(req, template, {
            "terms_form": terms_form,
            "listing_form": listing_form
        })
    
    # 5 Security logging
    logger.info("User %s accessed: Listing edit page.", "{req.user}")
    return redirect(req.META.get("HTTP_REFERER", "/"))

def listing_update_post(req: HttpRequest, pk: int, template: str):
    listing = listing_repo.find_by_pk(pk)
    terms = listing.terms

    # 4 Authentication & authorization
    if req.user == listing.poster:
        terms_form = TermsForm(req.POST, instance=terms)
        listing_form = ListingForm(req.POST, instance=listing)
        context = {
            "terms_form": terms_form,
            "listing_form": listing_form
        }

        # 2 Input validation & sanitization
        if not all([form.is_valid() for form in context.values()]):
            # 5 Security logging
            logger.error("Listing update failed due to validation errors.")
            return redirect(reverse("listing-detail", kwargs={"pk":pk}))

        items = listing_form.cleaned_data.pop("items")
        terms_repo.update(terms, terms_form.cleaned_data)
        listing_repo.update(items, listing, listing_form.cleaned_data)
        
        # 5 Security logging
        logger.info("User %s updated a listing with the ID %d.", f"{req.user}", pk)
        return render(req, template, context)
    
    return redirect(req.META.get("HTTP_REFERER", "/"))

def listing_update(req: HttpRequest, pk: int):
    template = "listings/listing_edit.html"
    return listing_update_post(req, pk, template) if req.method == "POST" else listing_update_get(req, pk, template)

def listing_detail(req: HttpRequest, pk: int):
    username = f"{req.user}" if req.user.is_authenticated else "'guest'"
    listing = listing_repo.find_by_pk(pk)

    # 5 Security logging
    logger.info("User %s accessed: Listing detail page.", username)
    return render(req, "listings/listing_detail.html", {"listing": listing})

def listing_delete(req: HttpRequest, pk: int):
    listing = listing_repo.find_by_pk(pk)
    terms = listing.terms
    
    # 4 Authentication & authorization
    if req.user == listing.poster:
        listing_repo.delete(listing)
        terms_repo.delete(terms)

        # 5 Security logging
        logger.warning("User %s deleted a listing with the ID %d.", f"{req.user}", pk)
        return redirect(reverse("listing-list"))
    
    return redirect(req.META.get("HTTP_REFERER", "/"))

# Other
def listing_search(req: HttpRequest):
    pass

def listing_save(req: HttpRequest, pk: int):
    listing = listing_repo.find_by_pk(pk)

    if req.user != listing.poster:
        # 5 Security logging
        logger.info("User %s saved a listing with the ID %d", f"{req.user}", pk)
        listing_repo.save(listing, req.user)
    
    return redirect(req.META.get("HTTP_REFERER", "/"))