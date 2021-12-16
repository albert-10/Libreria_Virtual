from django.forms.widgets import DateInput, Select, TextInput
from django.db.models import Avg
import django_filters
from .models import *
from django_filters import DateFilter

# La siguiente clase permite filtrar los libros por los campos: 'autor', 'nombre_editorial', 'despues_fecha', 'antes_fecha'
# Tambien permite ordenar el resultado de acuerdo a la calificacion promedio de los libros: ascendente o descendente

class Libro_Filter(django_filters.FilterSet):
	CHOICES = (
		('ascendente', 'ascendente'),
		('descendente', 'descendente'),
	)

	orden_por_calificacion = django_filters.ChoiceFilter(
		label='Ordenar por calificacion:',
		choices=CHOICES,
		method='filter_by_order',
		widget=Select(attrs={'class':'form-control', 'placeholder':'Sin orden'}),
	)

	despues_fecha = DateFilter(
		widget=DateInput(attrs={'type': 'date', 'class':'form-control'}),
		field_name="fecha_publicacion",
		lookup_expr='gt',
		label='Publicado despues de'
	)
	antes_fecha = DateFilter(
		widget=DateInput(attrs={'type': 'date', 'class':'form-control', 'placeholder':'Publicado antes de'}),
		field_name="fecha_publicacion",
		lookup_expr='lt',
		label='Publicado antes de'
	)

	nombre_editorial = django_filters.CharFilter(label='',
		widget=TextInput(attrs={'class':'form-control', 'placeholder':'Editorial'}))

	autor = django_filters.CharFilter(label='',
		field_name='autor__nombre',
		lookup_expr='iexact',
		widget=TextInput(attrs={'class':'form-control', 'placeholder':'Autor'}))
	

	class Meta:
		model = Libro
		fields = ['autor', 'nombre_editorial', 'despues_fecha', 'antes_fecha']		

	# Permite ordenar los libros de acuerdo a su calificacion promedio: ascendente o descendente

	def filter_by_order(self, queryset, name, value):
		if value == 'ascendente':
			queryset = queryset.annotate(calificacion_promedio=Avg('review__calificacion')).order_by('calificacion_promedio')
		else:
			queryset = queryset.annotate(calificacion_promedio=Avg('review__calificacion')).order_by('-calificacion_promedio')
		
		return queryset

# La siguiente clase permite filtrar los autores por los campos: 'nombre', 'nacionalidad', 'despues_fecha', 'antes_fecha'

class Autor_Filter(django_filters.FilterSet):

	despues_fecha = DateFilter(
		widget=DateInput(attrs={'type': 'date', 'class':'form-control'}),
		field_name="fecha_nacimiento",
		lookup_expr='gt',
		label='Nacido después de'
	)
	antes_fecha = DateFilter(
		widget=DateInput(attrs={'type': 'date', 'class':'form-control'}),
		field_name="fecha_nacimiento",
		lookup_expr='lt',
		label='Nacido antes de'
	)

	nombre = django_filters.CharFilter(label='',
		field_name='nombre',
		lookup_expr='iexact',
		widget=TextInput(attrs={'class':'form-control', 'placeholder':'Nombre'}))

	nacionalidad = django_filters.CharFilter(label='',
		field_name='nacionalidad',
		lookup_expr='iexact',
		widget=TextInput(attrs={'class':'form-control', 'placeholder':'Nacionalidad'}))

	class Meta:
		model = Autor
		fields = ['nombre', 'nacionalidad', 'despues_fecha', 'antes_fecha']

# La siguiente clase permite filtrar usuarios por nombre y username

class Usuario_Filter(django_filters.FilterSet):

	first_name = django_filters.CharFilter(label='',
		field_name='user__first_name',
		lookup_expr='iexact',
		widget=TextInput(attrs={'class':'form-control', 'placeholder':'Nombre'}))

	username = django_filters.CharFilter(label='',
		field_name='user__username',
		lookup_expr='exact',
		widget=TextInput(attrs={'class':'form-control', 'placeholder':'Username'}))

	class Meta:
		model = Usuario
		fields = ['first_name', 'username']

class Review_Filter(django_filters.FilterSet):	

	CHOICES_CALIFICACION = (
		(1, 1),
		(2, 2),
		(3, 3),
		(4, 4),
		(5, 5)
	)

	calificacion = django_filters.ChoiceFilter(
		label='Filtrar por calificacion:',
		choices=CHOICES_CALIFICACION,
		widget=Select(attrs={'class':'form-control', 'placeholder':'Sin orden'}),
	)

	CHOICES = (
		('ascendente', 'ascendente'),
		('descendente', 'descendente'),
	)

	# Permite ordenar los libros de acuerdo a su calificacion promedio: ascendente o descendente

	def filtrar_fecha_creacion(self, queryset, name, value):
		if value == 'ascendente':
			queryset = queryset.order_by('fecha_creada')
		else:
			queryset = queryset.order_by('-fecha_creada')
		return queryset

	fecha_creada = django_filters.ChoiceFilter(
		label='Fecha de creación',
		choices=CHOICES,
		method='filtrar_fecha_creacion',
		widget=Select(attrs={'class':'form-control'}))

	class Meta:
		model = Review
		fields = ['calificacion']