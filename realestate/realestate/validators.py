from datetime import date, datetime
from django.core.validators import BaseValidator, RegexValidator
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _

class AlphaValidator(RegexValidator):
    regex = r"^[a-zA-Z]*$"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class AdultValidator(BaseValidator):
    def __init__(self, limit_value=18, message=None):
        super().__init__(limit_value, message)

    def __call__(self, value):
        today = date.today()
        print(value)
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))

        if age < self.limit_value:
            raise ValidationError(_("birth_date.adult"))

class AfterOrEqual(BaseValidator):
    def __init__(self, limit_value=date.today(), message=None):
        super().__init__(limit_value, message)
    
    def __call__(self, value):
        if value < self.limit_value:
            raise ValidationError(_("move_in_date.after_or_equal"))