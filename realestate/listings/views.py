from django.core.paginator import Paginator
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import generic

from .forms import TermsForm, ListingForm
from .helpers.dropdowns import order_list
from .models import Listing
from .repositories import terms_repo, listing_repo

# Create your views here.
def listing_list(req: HttpRequest):
    order = req.GET.get("redosled") if "redosled" in req.GET else ""
    page = req.GET.get("strana")

    listings = listing_repo.find_all(order)
    paginator = Paginator(listings, per_page=2)
    listings = paginator.get_page(page)
    return render(req, "listings/listing_list.html", {
        "order_list": order_list,
        "listings": listings
    })

def listing_create_get(req: HttpRequest, template):
    terms_form = TermsForm()
    listing_form = ListingForm()
    return render(req, template, {
        "terms_form": terms_form,
        "listing_form": listing_form
    })

def listing_create_post(req: HttpRequest, template):
    terms_form = TermsForm(req.POST)
    listing_form = ListingForm(req.POST)
    forms = {
        "terms_form": terms_form,
        "listing_form": listing_form
    }
    
    # 2 Input validation & sanitization
    if all([form.is_valid() for form in forms.values()]):
        items = listing_form.cleaned_data.pop("items")
        terms = terms_repo.find_or_create(terms_form.cleaned_data)
        poster = req.user
        listing_repo.create(items, terms, poster, listing_form.cleaned_data)
        return redirect(reverse("listing-list"))

    return render(req, template, forms)    

def listing_create(req: HttpRequest):
    template = "listings/listing_create.html"
    return listing_create_post(req, template) if req.method == "POST" else listing_create_get(req, template)

class ListingDetailView(generic.DetailView):
    model = Listing

class ListingUpdateView(generic.UpdateView):
    model = Listing
    template_name = "listings/listing_edit.html"

    def get(self, request: HttpRequest, pk):
        listing: Listing = self.get_object()
        terms = listing.terms
        
        # 3 Authentication and authorization (role-based)
        if request.user == listing.poster:
            terms_form = TermsForm(instance=terms)
            listing_form = ListingForm(instance=listing)
            return render(request, self.template_name, {
                "terms_form": terms_form,
                "listing_form": listing_form
            })
        
        return redirect(reverse("listing-detail", kwargs={"pk": pk}))

    def post(self, request: HttpRequest, pk):
        listing: Listing = self.get_object()
        terms = listing.terms

        # 3 Authentication and authorization (role-based)
        if request.user == listing.poster:
            terms_form = TermsForm(request.POST, instance=terms)
            listing_form = ListingForm(request.POST, instance=listing)
            context = {
                "terms_form": terms_form,
                "listing_form": listing_form
            }

            # 2 Input validation & sanitization
            if all([form.is_valid() for form in context.values()]):
                items = listing_form.cleaned_data.pop("items")
                terms_repo.update(terms, terms_form.cleaned_data)
                listing_repo.update(items, listing, listing_form.cleaned_data)
                return redirect(reverse("listing-detail", kwargs={"pk":pk}))
            
            return render(request, self.template_name, context)
        
        return redirect(reverse("listing-edit", kwargs={"pk":pk}))

def listing_delete(req: HttpRequest, pk):
    listing = listing_repo.find_by_pk(pk)
    terms = listing.terms
    
    # 3 Authentication and authorization (role-based)
    if req.user == listing.poster:
        listing_repo.delete(listing)
        terms_repo.delete(terms)
        return redirect(reverse("listing-list"))
    
    return redirect(reverse("listing-detail", kwargs={"pk":pk}))

def listing_save(req: HttpRequest, pk):
    listing = listing_repo.find_by_pk(pk)

    print(req.user != listing.poster)

    if req.user != listing.poster:
        listing_repo.save(listing, req.user)
    
    return redirect(req.META.get("HTTP_REFERER", "/"))

class ListingSearchView(generic.ListView):
    model = Listing
    context_object_name = "listings"
    page_kwarg = "strana"
    paginate_by = 2
    
    def get_queryset(self):
        order = self.request.GET.pop("redosled") if "redosled" in self.request.GET else ""
        query = filter(self.request.GET)
        return Listing.objects.all()