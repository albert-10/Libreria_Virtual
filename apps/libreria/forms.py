from django import forms
from django.forms import widgets
from .models import Autor, Libro

class LibroForm(forms.ModelForm):

    class Meta:
            model = Libro
            fields = '__all__'
            widgets = {
                'fecha_publicacion': forms.DateInput(attrs={'type':'date'})
            }

class AutorForm(forms.ModelForm):

    class Meta:
            model = Autor
            fields = '__all__'
            widgets = {
                'fucha_nacimiento': forms.DateInput(attrs={'type':'date'})
            }

# class LibroEditarForm(forms.ModelForm):

#     class Meta:
#             model = Libro
#             fields = '__all__'
#             widgets = {
#                 'fecha_publicacion': forms.DateInput(attrs={'type':'date'})
#             }

    # def __init__(self, *args, **kwargs):
    #     self.libro_id = kwargs.pop('libro_id')
    #     # product = Product.objects.get(id=self.product_id)
    #     super().__init__(*args, **kwargs)