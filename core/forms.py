from django import forms
from core.models import Stack


class StackForm(forms.ModelForm):

    class Meta:
        model = Stack
        fields = ('name',)
