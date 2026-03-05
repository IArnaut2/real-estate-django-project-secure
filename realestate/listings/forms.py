from django import forms
from django.core.validators import MinValueValidator, RegexValidator
from django.utils.translation import gettext_lazy as _

from realestate.validators import AfterOrEqual

from .helpers.dropdowns import city_list, condition_list, heating_list, furnishings_list
from .models import Terms, Listing

class TermsForm(forms.ModelForm):
    move_in_date = forms.DateField(
        required=True,
        # 2 Input validation & sanitization
        error_messages={"required":_("field.required").format(field=_("move_in_date"))},
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"})
    )

    class Meta:
        model = Terms
        fields = "__all__"
    
    def __init__(self, *args, **kwargs):
        super(TermsForm, self).__init__(*args, **kwargs)

        # 2 Input validation & sanitization
        self.fields["move_in_date"].validators = [AfterOrEqual()]

        for field in ["deposit", "for_students", "for_workers", "smoking_allowed", "pets_allowed"]:
            self.fields[field].widget.attrs["class"] = "form-check-input"

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = "__all__"
        exclude = ["terms", "poster"]
        widgets = {
            "city": forms.Select(choices=city_list),
            "condition": forms.Select(choices=condition_list),
            "heating": forms.Select(choices=heating_list),
            "furnishings": forms.Select(choices=furnishings_list),
        }
    
    def __init__(self, *args, **kwargs):
        super(ListingForm, self).__init__(*args, **kwargs)

        # 2 Input validation & sanitization
        self.fields["street"].validators = [RegexValidator(r"^[\w\d. ]+$", _("street.regex").format(field="street"))]
        self.fields["story_count"].validators = [MinValueValidator(1, _("story_count.min").format(field="story_count"))]
        self.fields["room_count"].validators = [MinValueValidator(0, _("room_count.min").format(field="room_count"))]
        self.fields["area"].validators = [MinValueValidator(10, _("area.min").format(field="area"))]
        self.fields["story"].validators = [MinValueValidator(0, _("story.min").format(field="story"))]
        self.fields["price"].validators = [MinValueValidator(100, _("price.min").format(field="price"))]

        for field in ["street", "story_count", "room_count", "area", "story", "title", "price", "description"]:
            self.fields[field].widget.attrs["class"] = "form-control"
            # 2 Input validation & sanitization
            self.fields[field].error_messages = {"required": _("field.required").format(field=_(field))}

        for field in ["city", "condition", "heating", "furnishings", "items"]:
            self.fields[field].widget.attrs["class"] = "form-select"

        for field in ["elevator", "parking", "garage", "cctv", "intercom"]:
            self.fields[field].widget.attrs["class"] = "form-check-input"