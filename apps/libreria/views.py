from django.views.generic import View
from django.http.response import HttpResponse
from django.shortcuts import reverse, get_object_or_404
from django.views import generic
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic.edit import  UpdateView, DeleteView
from .filters import Libro_Filter
from .models import Libro
from .forms import LibroForm


# La siguiente vista retorna libros segun el filtro que realice el usuario

class LibrosView(generic.ListView):
    model = Libro
    template_name = 'libreria/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['libro_filter'] = Libro_Filter(self.request.GET, queryset=self.get_queryset())
        return context

# La siguiente vista retorna libros segun el filtro que realice el admin

class LibrosAdminView(generic.ListView):
    model = Libro
    template_name = 'libreria/librosAdmin.html'

# El siguiente metodo permite obtener un page de libro,
# de acuerdo al filtro de libros que se haya aplicado

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        libro_filter = Libro_Filter(self.request.GET, queryset=self.get_queryset())
        context['libro_filter'] = libro_filter
        libros_filtrados_paginados = Paginator(libro_filter.qs, 2)
        page_number = self.request.GET.get('page')
        libro_page = libros_filtrados_paginados.get_page(page_number)
        context['libro_page'] = libro_page
        return context

# La siguiente vista pemite insertar usuarios

class InsertarLibroView(generic.FormView):
    template_name = 'libreria/insertarLibro.html'
    form_class = LibroForm

    def get_success_url(self):
        return reverse("libreria:insertarLibro")

    def form_valid(self, form):
        
        form.save(commit=True)
        return super(InsertarLibroView, self).form_valid(form)

# La siguiente clase permite editar Libros

class EditarLibroView(UpdateView):
    template_name = 'libreria/editarLibro.html'
    model = Libro
    fields = '__all__'

    def get_object(self):
        return get_object_or_404(Libro, pk=self.kwargs["pk"])

    def form_valid(self, form):        
        form.save(commit=True)
        return super().form_valid(form)

# La siguiente clase permite eliminar Libros

class EliminarLibroView(DeleteView):    
    model = Libro
    success_url = reverse_lazy('libreria:librosAdmin')
