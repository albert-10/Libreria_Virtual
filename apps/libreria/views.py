import os
from django.views.generic import View
from django.http.response import HttpResponse
from django.shortcuts import reverse, get_object_or_404
from django.views import generic
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic.edit import  UpdateView, DeleteView, CreateView
from .filters import Libro_Filter
from .models import Libro, Autor
from .forms import LibroForm, AutorForm


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

# Antes de editar el libro se comprueba que en el formulario haya un nuevo archivo. Si es asi se elimina
# el antiguo archivo antes de guardar la edicion del libro

    def form_valid(self, form):
        if len(self.request.FILES) > 0:
            libro = self.get_object()
            os.remove(libro.archivo_libro.path)
        
        form.save(commit=True)
        return super().form_valid(form)

# La siguiente clase permite eliminar Libros

class EliminarLibroView(DeleteView):    
    model = Libro
    success_url = reverse_lazy('libreria:librosAdmin')

# La siguiente vista pemite insertar autores

class InsertarAutorView(CreateView):
    template_name = 'libreria/insertarAutor.html'
    form_class = AutorForm
    queryset = Autor.objects.all()

    def get_success_url(self):
        return reverse("libreria:insertarAutor")

    def form_valid(self, form):       
        return super().form_valid(form)
