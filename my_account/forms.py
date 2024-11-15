
from django.forms import ModelForm, TextInput, EmailInput, ClearableFileInput
from my_account.models import CustomUser

class AccountForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'avatar']
        widgets = {
            'username': TextInput(attrs={"class": "form-control", "type": "text", "name": "username"}),
            'avatar': ClearableFileInput(attrs={"class": "form-control", "name": "avatar"}),
        }
