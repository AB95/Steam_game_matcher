__author__ = 'Dean'

from django import forms


class UserIDForm(forms.Form):
    user_ID_1 = forms.CharField(max_length=255)
    user_ID_2 = forms.CharField(max_length=255)

