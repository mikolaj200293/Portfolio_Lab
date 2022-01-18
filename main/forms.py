from django import forms


class AddUserForm(forms.Form):
    """
    Create user creating form.
    """
    password = forms.CharField(max_length=100, label='Hasło', widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=100, label='Potwierdź hasło', widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=100, label='Imię')
    last_name = forms.CharField(max_length=100, label='Nazwisko')
    mail = forms.EmailField(max_length=100, label='Adres Email')