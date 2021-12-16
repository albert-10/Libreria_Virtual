from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import widgets
from .models import Autor, Libro, Usuario, Review

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
    first_name = forms.CharField()
    username = forms.CharField()
    email = forms.EmailField()
    password_confirm = forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(widget=forms.PasswordInput)
    is_admin = forms.BooleanField(required=False, label='¿Es administrador?')
   
    class Meta:
            model = Usuario
            fields = ['first_name', 'username', 'email', 'password', 'password_confirm','imagen','is_admin']
                
#La siguiente funcionalidad agrega un error al formulario si los passwords no coinciden

    def clean(self):
        cleaned_data = super(UsuarioForm, self).clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")       
        if password != password_confirm:                     
            self.add_error('password', "Passwords no coinciden")
            self.add_error('password_confirm', "Passwords no coinciden")

class AutenticarForm(forms.Form):

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
   
    # class Meta:            
    #         fields = ['first_name', 'email', 'username', 'password', 'password_confirm','imagen','is_admin']

# class SignUpForm(UserCreationForm):
#     class Meta:
#         model = Usuario
#         fields = ('email',)

# class AutenticarForm(forms.Form):

#     username = forms.TimeField()
#     password = forms.CharField(widget=forms.PasswordInput)
   
#     class Meta:
#             model = Usuario
#             fields = ['username', 'password']

class ReviewForm(forms.Form):   
    opinion = forms.CharField(widget=forms.Textarea(attrs={'class': 'noVisible'}))
    CALIFICACIONES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5)
    )
    calificacion = forms.ChoiceField(choices=CALIFICACIONES, label='')
    # class Meta:
    #         model = Review
    #         fields = '__all__'