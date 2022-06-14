from django import forms
from django.contrib.auth import get_user_model
from . import models


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ('picture',)
