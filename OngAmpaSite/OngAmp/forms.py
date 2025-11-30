# OngAmp/forms.py
from django import forms
from .models import Adotante


class CadastroAdotanteForm(forms.ModelForm):
    class Meta:
        model = Adotante
        fields = ['nome', 'cpf', 'telefone', 'email', 'endereco']
        
        # Vamos deixar o formulário bonito com classes CSS
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seu nome completo'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apenas números'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(XX) 99999-9999'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'seu@email.com'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rua, Número, Bairro'}),
        }