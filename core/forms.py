from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Avaliacao

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Digite seu usuário'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Digite sua senha'
        })


class AvaliacaoForm(forms.ModelForm):

    class Meta:
        model = Avaliacao
        fields = ['nome', 'nota', 'comentario']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite seu nome',
            }),
            
            'nota': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite uma nota',
                'min': 0,
                'max': 10,
            }),

            'comentario': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Faça um comentário',
            }),
        }
