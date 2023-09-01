from django import forms

from games.models import Game
from users.models import User

class NewComentatorForm(forms.Form):
    name = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'class': 'border rounded w-full py-2 px-4'})
    )
    game = forms.ModelChoiceField(
        queryset=Game.objects.all(),
        widget=forms.Select(attrs={'class': 'border rounded w-full py-2 px-4'})
    )
    