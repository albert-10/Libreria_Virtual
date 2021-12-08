from django.forms.widgets import DateInput
import django_filters
from .models import *
from django_filters import DateFilter

class Libro_Filter(django_filters.FilterSet):
	despues_fecha = DateFilter(
		widget=DateInput(attrs={'type': 'date', 'class':'form-horizontal'}),
		field_name="fecha_publicacion",
		lookup_expr='gt',
		label='Publicado despues de:'
	)
	antes_fecha = DateFilter(
		widget=DateInput(attrs={'type': 'date'}),
		field_name="fecha_publicacion",
		lookup_expr='lt',
		label='Publicado despues de:'
	)

	nombre_editorial = django_filters.CharFilter(label='Editorial')

	class Meta:
		model = Libro
		fields = '__all__'
		exclude = ['titulo', 'date_created', 'cantidad_paginas', 'fecha_publicacion','isbn']	

