from django.shortcuts import render
from django.views import generic
from django.db.models import Avg
from .models import Libro
from .filters import Libro_Filter

""" class Home(generic.TemplateView):
    template_name = 'libreria/home.html' """

""" class HomeView(generic.ListView):
    template_name='libreria/home.html'
    queryset = Libro.objects.all() """

# La siguiente vista retorna libros segun el filtro que realice el usuario

class HomeView(generic.View):
    def get(self, request):
        ordenar_calificacion_ascendente = 'ordenado' in list(request.GET.keys()) 
        libros = Libro.get_libros_ordenados(ordenar_calificacion_ascendente)
        
        libro_filter = Libro_Filter(request.GET, queryset=libros)
        libros = libro_filter.qs
        context = {'libros':libros, 'libro_filter': libro_filter}
        return render(request, 'libreria/home.html',context)

""" def libros_filtrados(request):    
    ordenar_calificacion_ascendente = 'ordenado' in list(request.GET.keys()) 
    libros = Libro.get_libros_ordenados(ordenar_calificacion_ascendente)
    
    libro_filter = Libro_Filter(request.GET, queryset=libros)
    libros = libro_filter.qs
    context = {'libros':libros, 'libro_filter': libro_filter}
    return render(request, 'libreria/home.html',context) """
