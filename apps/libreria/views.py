import os
from django.shortcuts import reverse, get_object_or_404
from django.views import generic
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic.edit import  UpdateView, DeleteView, CreateView
from .filters import Libro_Filter, Autor_Filter, Usuario_Filter
from .models import Libro, Autor, Usuario
from .forms import LibroForm, AutorForm, UsuarioForm
from django.contrib.auth import get_user_model

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
        libros_filtrados_paginados = Paginator(libro_filter.qs, 5)
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

class ListarAutoresView(generic.ListView):
    model = Autor
    template_name = 'libreria/listarAutores.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # lista_Inputs = list(self.request.GET.keys())
               
        # if 'numeroAutores' in lista_Inputs:
        #     if self.request.GET['numeroAutores'] != '':                
        #         autores_por_pagina = int(self.request.GET['numeroAutores'])
        #     else:
        #         autores_por_pagina = 2
        # else:
        #     autores_por_pagina = 2
        autor_filter = Autor_Filter(self.request.GET, queryset=self.get_queryset())
        context['autor_filter'] = autor_filter
        autores_filtrados_paginados = Paginator(autor_filter.qs, 5)
        
        
        # if 'numeroDePagina' in lista_Inputs:
        #     if self.request.GET['numeroDePagina'] != '':
        #         numero_de_pagina = int(self.request.GET['numeroDePagina'])
        #     else:
        #         numero_de_pagina = None
        # else:
        numero_de_pagina = self.request.GET.get('page')

        autor_page = autores_filtrados_paginados.get_page(numero_de_pagina)
        context['autor_page'] = autor_page
        return context

class DetallesAutorView(generic.DetailView):
    template_name = 'libreria/detallesAutor.html'
    queryset = Autor.objects.all()
    context_object_name = 'autor'

class EliminarAutorView(DeleteView):    
    model = Autor
    success_url = reverse_lazy('libreria:listarAutores')

class EditarAutorView(UpdateView):
    template_name = 'libreria/editarAutor.html'
    form_class = AutorForm
    model = Autor    

    def get_object(self):
        return get_object_or_404(Autor, pk=self.kwargs["pk"])

# La siguiente clase permite listar usuarios, tambien filtrarlos y paginarlos

class ListarUsuariosView(generic.ListView):
    model = Usuario
    template_name = 'libreria/listarUsuarios.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
       
        usuario_filter = Usuario_Filter(self.request.GET, queryset=self.get_queryset())
        context['usuario_filter'] = usuario_filter
        usuarios_filtrados_paginados = Paginator(usuario_filter.qs, 5)
       
        numero_de_pagina = self.request.GET.get('page')
        usuario_page = usuarios_filtrados_paginados.get_page(numero_de_pagina)
        context['usuario_page'] = usuario_page
        return context

class InsertarUsuarioView(generic.FormView):
    template_name = 'libreria/insertarUsuario.html'
    form_class = UsuarioForm
    queryset = Usuario.objects.all()    

    def get_success_url(self):
        return reverse("libreria:insertarUsuario")

    def form_valid(self, form):
        User = get_user_model()
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        nombre = form.cleaned_data['nombre']

        user = User.objects.create(username=username, first_name=nombre)
        user.set_password(password)
        user.save()
        
        imagen = form.cleaned_data['imagen']
        Usuario.objects.create(imagen=imagen, user=user)

        print(form.cleaned_data)   
        return super().form_valid(form)