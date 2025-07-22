from django import forms
from .models import CompanyProfile

class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = [
            'name', 'address', 'phone', 'email',
            'bank_name', 'bank_account_name', 'iban', 'swift_code'
        ]


class EmailForm(forms.Form):
    recipient_email = forms.EmailField(label="Client Email")
