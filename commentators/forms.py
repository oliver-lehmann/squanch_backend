from django import forms

from games.models import Game
from users.models import User

class NewComentatorForm(forms.Form):
    name = forms.ModelChoiceField(queryset=User.objects.all())
    game = forms.ModelChoiceField(queryset=Game.objects.all())
    