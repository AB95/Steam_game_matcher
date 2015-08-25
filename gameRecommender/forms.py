__author__ = 'Dean'

from django import forms
from gameRecommender import models


class UserIDForm(forms.Form):
    user_ID_1 = forms.CharField(max_length=255)
    user_ID_2 = forms.CharField(max_length=255)


# class TagForm(forms.Form):
#     tags = []
#     for item in models.GameTags.tags:
#         tags.append(forms.RadioSelect())

class TagForm(forms.Form):
    list = []
    for item in models.GameTags.objects.values('tags'):
        list.append((item['tags'], item['tags']))

    tags = forms.ChoiceField(choices=list, widget=forms.CheckboxSelectMultiple())
