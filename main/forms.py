from django import forms
from django.core.validators import EmailValidator
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField

User = get_user_model()


class AddUserForm(forms.Form):
    """
    Create user creating form.
    """
    password = forms.CharField(max_length=100, label='Hasło', widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=100, label='Potwierdź hasło', widget=forms.PasswordInput)
    name = forms.CharField(max_length=100, label='Imię')
    surname = forms.CharField(max_length=100, label='Nazwisko')
    email = forms.EmailField(max_length=100, label='Adres Email', validators=[EmailValidator()])


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=100, label='Adres Email', validators=[EmailValidator()])
    password = forms.CharField(max_length=100, label='Hasło', widget=forms.PasswordInput)


class DonationForm(forms.Form):
    categories = forms.IntegerField(min_value=1)
    bags = forms.IntegerField(min_value=1, max_value=100)
    organization = forms.CharField(max_length=100)
    address = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    postcode = forms.CharField(max_length=10)
    phone = forms.CharField()
    data = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d'))
    time = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
    more_info = forms.Textarea()


class ArchiveForm(forms.Form):
    donation_id = forms.IntegerField()
    is_taken = forms.NullBooleanField()
