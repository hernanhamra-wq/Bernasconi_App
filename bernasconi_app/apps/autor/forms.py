from django import forms
from .models import Autor


class AutorForm(forms.ModelForm):
    class Meta:
        model = Autor
        fields = ['nombre', 'biografia']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del autor',
                'autofocus': True
            }),
            'biografia': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Biografía (opcional)',
                'rows': 4
            }),
        }
