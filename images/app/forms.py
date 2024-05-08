from django import forms

from .models import Image


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['name', 'file']


class EditImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['name']
