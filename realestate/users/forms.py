from django import forms
from django.core.validators import EmailValidator, RegexValidator
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from realestate.validators import AdultValidator, AlphaValidator

from .models import CustomUser

class UserUpdateForm(UserCreationForm):
    curr_password = forms.CharField()

    class Meta:
        model = CustomUser
        fields = ["email", "password1", "password2"]
        error_messages = {
            "email": {"required": _("field.required").format(field="email")},
            "curr_password": {"required": _("field.required").format(field="curr_password")}
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 2 Input validation & sanitization
        self.fields["email"].validators = [EmailValidator(message=_("email.email"))]

        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"

    # 2 Input validation & sanitization
    def clean_password2(self):
        pass1 = self.cleaned_data["password1"]
        pass2 = self.cleaned_data["password2"]

        if pass1 and pass2 and pass1 != pass2:
            raise forms.ValidationError(_("password2.confirmed"))

        return pass2

class UserUpdate2Form(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["phone", "first_name", "last_name", "birth_date"]
        error_messages = {
            "phone": {"required": _("field.required").format(field="phone")},
            "first_name": {"required": _("field.required").format(field="first_name")},
            "last_name": {"required": _("field.required").format(field="last_name")},
            "birth_date": {"required": _("field.required").format(field="birth_date")}
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 2 Input validation & sanitization
        self.fields["phone"].validators = [RegexValidator(regex=r"^\+381 \d{2} \d{6,7}$", message=_("phone.regex"))]
        self.fields["first_name"].validators = [AlphaValidator(_("field.alpha").format(field="first_name"))]
        self.fields["last_name"].validators = [AlphaValidator(_("field.alpha").format(field="last_name"))]
        self.fields["birth_date"].validators = [AdultValidator]

        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"

class UserDeleteForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))

    class Meta:
        model = CustomUser
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 2 Input validation & sanitization
        self.fields["password"].error_messages = {"required": _("field.required").format(field="password")}
