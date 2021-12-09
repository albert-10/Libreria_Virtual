from django.shortcuts import render
from django.views import generic
from django.db.models import Avg
from .models import Libro
from .filters import Libro_Filter

# La siguiente vista retorna libros segun el filtro que realice el usuario

class LibrosView(generic.ListView):
    model = Libro
    template_name = 'libreria/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['libro_filter'] = Libro_Filter(self.request.GET, queryset=self.get_queryset())
        return context


# class HomeView(generic.View):
#     def get(self, request):
#         # ordenar_calificacion_ascendente = 'ordenado' in list(request.GET.keys()) 
#         # libros = Libro.get_libros_ordenados(ordenar_calificacion_ascendente)
#         libros = Libro.objects.all()
#         libro_filter = Libro_Filter(request.GET, queryset=libros)
#         libros = libro_filter.qs
#         context = {'libros':libros, 'libro_filter': libro_filter}
#         return render(request, 'libreria/home.html',context)
