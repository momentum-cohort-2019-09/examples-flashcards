from django import forms
from core.models import Stack, Card


class StackForm(forms.ModelForm):

    class Meta:
        model = Stack
        fields = ('name',)


class CardForm(forms.ModelForm):

    class Meta:
        model = Card
        fields = (
            'prompt',
            'answer',
        )


class CardResultsForm(forms.Form):
    correct = forms.BooleanField(required=False)
