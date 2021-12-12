from django import forms
from django.forms import widgets
from .models import Autor, Libro, Usuario

class LibroForm(forms.ModelForm):

    class Meta:
            model = Libro
            fields = '__all__'
            widgets = {
                'fecha_publicacion': forms.DateInput(attrs={'type':'date'}),
                'cantidad_paginas': forms.NumberInput(attrs={'min': '1'})
            }

class AutorForm(forms.ModelForm):

    class Meta:
            model = Autor
            fields = '__all__'
            widgets = {
                'fecha_nacimiento': forms.DateInput(attrs={'type':'date'})
            }

class UsuarioForm(forms.ModelForm):
    nombre = forms.CharField()
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
            model = Usuario
            fields = ['imagen']          