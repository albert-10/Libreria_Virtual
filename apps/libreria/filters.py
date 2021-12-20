from django.forms.widgets import DateInput, NumberInput, Select, TextInput
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
		label='Calificación',
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

	offset = django_filters.NumberFilter(
		label='',
		method='a_partir_de_usuario',
		widget=NumberInput(attrs={'class':'form-control', 'placeholder':'A partir del libro', 'min': '1', 'step': '1'})
	)

	limit = django_filters.NumberFilter(
		label='',		
		method='cantidad_usuarios',
		widget=NumberInput(attrs={'class':'form-control', 'placeholder':'Cantidad de libros', 'min': '1', 'step': '1'})
	)

	# Permite ordenar los libros de acuerdo a su calificacion promedio: ascendente o descendente

	def filter_by_order(self, queryset, name, value):
		if value == 'ascendente':
			queryset = queryset.annotate(calificacion_promedio=Avg('review__calificacion')).order_by('calificacion_promedio')
		else:
			queryset = queryset.annotate(calificacion_promedio=Avg('review__calificacion')).order_by('-calificacion_promedio')
		
		return queryset

	# Permite obtener los usuarios a partir el usuario value - 1, 
	
	def a_partir_de_usuario(self, queryset, name, value):		
		return queryset[value - 1:]

	# Permite obtener value cantidad de usuarios

	def cantidad_usuarios(self, queryset, name, value):
		return queryset[:value]	
	

	class Meta:
		model = Libro
		fields = ['autor', 'nombre_editorial', 'despues_fecha', 'antes_fecha']		

	

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

	limit = django_filters.NumberFilter(
		label='',		
		method='cantidad_usuarios',
		widget=NumberInput(attrs={'class':'form-control', 'placeholder':'Cantidad de usuarios', 'min': '1', 'step': '1'})
	)

	# Permite obtener value cantidad de usuarios

	def cantidad_usuarios(self, queryset, name, value):
		return queryset[:value]	

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
		label='Ordenar por Fecha',
		choices=CHOICES,
		method='filtrar_fecha_creacion',
		widget=Select(attrs={'class':'form-control'}))

	class Meta:
		model = Review
		fields = ['calificacion']

# La siguiente clase permite filtrar las review de un libro

class Review_Libro_Filter(django_filters.FilterSet):	

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
		label='Ordenar por fecha',
		choices=CHOICES,
		method='filtrar_fecha_creacion',
		widget=Select(attrs={'class':'form-control'}))

	offset = django_filters.NumberFilter(
		label='',
		method='a_partir_de_reviwes',
		widget=NumberInput(attrs={'class':'form-control', 'placeholder':'A partir de la review', 'min': '1', 'step': '1'})
	)

	limit = django_filters.NumberFilter(
		label='',		
		method='cantidad_reviews',
		widget=NumberInput(attrs={'class':'form-control', 'placeholder':'Cantidad de reviews', 'min': '1', 'step': '1'})
	)

	# Permite ordenar los libros de acuerdo a su calificacion promedio: ascendente o descendente

	def filter_by_order(self, queryset, name, value):
		if value == 'ascendente':
			queryset = queryset.annotate(calificacion_promedio=Avg('review__calificacion')).order_by('calificacion_promedio')
		else:
			queryset = queryset.annotate(calificacion_promedio=Avg('review__calificacion')).order_by('-calificacion_promedio')
		
		return queryset

	# Permite obtener los usuarios a partir el usuario value - 1, 
	
	def a_partir_de_reviwes(self, queryset, name, value):		
		return queryset[value - 1:]

	# Permite obtener value cantidad de usuarios

	def cantidad_reviews(self, queryset, name, value):
		return queryset[:value]	

	class Meta:
		model = Review
		fields = ['calificacion']