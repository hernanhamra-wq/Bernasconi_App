from django import forms
from .models import CatalogoMultimedia


class MultimediaForm(forms.ModelForm):
    class Meta:
        model = CatalogoMultimedia
        fields = ['ficha', 'archivo', 'tipo', 'descripcion']
        widgets = {
            'ficha': forms.Select(attrs={'class': 'form-control'}),
            'archivo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
        }


class MultimediaFichaForm(forms.ModelForm):
    """Form para subir multimedia desde el detalle de una ficha (sin selector de ficha)."""
    class Meta:
        model = CatalogoMultimedia
        fields = ['archivo', 'tipo', 'descripcion']
        widgets = {
            'archivo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descripción opcional'}),
        }
