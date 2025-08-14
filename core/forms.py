from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Avaliacao

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(label="Nome", max_length=30, required=False)
    last_name  = forms.CharField(label="Sobrenome", max_length=30, required=False)
    email      = forms.EmailField(label="E-mail", required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Remove help_texts longos e adiciona classes/placeholders
        field_cfg = {
            "username":  {"ph": "Seu nome de usuário"},
            "first_name":{"ph": "Seu nome"},
            "last_name": {"ph": "Seu sobrenome"},
            "email":     {"ph": "seu@email.com", "type": "email", "autocomplete": "email"},
            "password1": {"ph": "Crie uma senha", "type": "password", "autocomplete": "new-password"},
            "password2": {"ph": "Confirme a senha", "type": "password", "autocomplete": "new-password"},
        }
        for name, f in self.fields.items():
            f.help_text = ""
            f.widget.attrs.update({
                "class": "form-input",
                "placeholder": field_cfg.get(name, {}).get("ph", ""),
                "autocomplete": field_cfg.get(name, {}).get("autocomplete", "off"),
                "type": field_cfg.get(name, {}).get("type", f.widget.input_type if hasattr(f.widget, "input_type") else "text")
            })

    def clean_email(self):
        email = self.cleaned_data["email"].lower().strip()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Já existe um usuário com este e-mail.")
        return email
    

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
