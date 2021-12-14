from django import forms
from django.contrib.auth.forms import UserCreationForm
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

# class UsuarioForm(forms.ModelForm):
#     password_confirm = forms.CharField(widget=forms.PasswordInput)
#     password = forms.CharField(widget=forms.PasswordInput)
   
#     class Meta:
#             model = Usuario
#             fields = ['first_name', 'email', 'user_username', 'user_password', 'password_confirm','imagen','user_is_admin']
                
# #La siguiente funcionalidad agrega un error al formulario si los passwords no coinciden

#     def clean(self):
#         cleaned_data = super(UsuarioForm, self).clean()
#         password = cleaned_data.get("password")
#         password_confirm = cleaned_data.get("password_confirm")       
#         if password != password_confirm:          
#             self.add_error('password', "Password does not match")
#             self.add_error('password_confirm', "Password does not match")

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