from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import EmailValidator, RegexValidator
from django.utils.translation import gettext_lazy as _

from realestate.validators import AdultValidator, AlphaValidator
from users.models import CustomUser

# 4 Authentication & authorization
class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["email", "password1", "password2", "phone", "first_name", "last_name", "birth_date"]
        # error_messages = {
        #     "email": {"required": _("field.required").format(field=_("email"))},
        #     "phone": {"required": _("field.required").format(field=_("phone"))},
        #     "first_name": {"required": _("field.required").format(field=_("first_name"))},
        #     "last_name": {"required": _("field.required").format(field=_("last_name"))},
        #     "birth_date": {"required": _("field.required").format(field=_("birth_date"))}
        # }
        widgets = {"birth_date": forms.DateInput(attrs={"type": "date"})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 2 Input validation & sanitization
        self.fields["password1"].error_messages = {"required": _("field.required").format(field=_("password1"))}
        self.fields["password2"].error_messages = {"required": _("field.required").format(field=_("password2"))}
        self.fields["email"].validators = [EmailValidator(message=_("email.email").format(field=_("email")))]
        self.fields["phone"].validators = [RegexValidator(regex=r"^\+381 \d{2} \d{6,7}$", message=_("phone.regex"))]
        self.fields["first_name"].validators = [AlphaValidator(message=_("field.alpha").format(field=_("first_name")))]
        self.fields["last_name"].validators = [AlphaValidator(message=_("field.alpha").format(field=_("last_name")))]
        self.fields["birth_date"].validators = [AdultValidator()]

        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"
            self.fields[field].error_messages = {"required": _("field.required").format(field=_(field))}
        
    # 2 Input validation & sanitization
    def clean_password2(self):
        pass1 = self.cleaned_data["password1"]
        pass2 = self.cleaned_data["password2"]

        if pass1 and pass2 and pass1 != pass2:
            raise forms.ValidationError(_("password2.confirmed"))

        return pass2


class LoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 2 Input validation & sanitization
        self.fields["username"].validators = [EmailValidator(message=_("email.email"))]
        
        for field in self.fields:
            self.fields[field].error_messages = {"required": _("field.required").format(field)}
            self.fields[field].widget.attrs["class"] = "form-control"