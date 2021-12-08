from django.forms.widgets import DateInput
import django_filters
from .models import *
from django_filters import DateFilter

class Libro_Filter(django_filters.FilterSet):
	despues_fecha = DateFilter(
		widget=DateInput(attrs={'type': 'date', 'class':'form-control'}),
		field_name="fecha_publicacion",
		lookup_expr='gt',
		label='Publicado despues de:'
	)
	antes_fecha = DateFilter(
		widget=DateInput(attrs={'type': 'date', 'class':'form-control'}),
		field_name="fecha_publicacion",
		lookup_expr='lt',
		label='Publicado despues de:'
	)

	nombre_editorial = django_filters.CharFilter(label='Editorial', widget=DateInput(attrs={'class':'form-control'}))
	autor = django_filters.CharFilter(label='Autor', field_name='autor__nombre', lookup_expr='iexact', widget=DateInput(attrs={'class':'form-control'}))

	class Meta:
		model = Libro
		fields = ['autor', 'nombre_editorial', 'despues_fecha', 'antes_fecha']			

