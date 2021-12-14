import os
from django.shortcuts import redirect, reverse, get_object_or_404
from django.http import HttpResponseRedirect
from django.views import generic
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.views.generic.detail import DetailView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import  UpdateView, DeleteView, CreateView
from .filters import Libro_Filter, Autor_Filter, Usuario_Filter
from .models import Libro, Autor, Usuario
from .forms import LibroForm, AutorForm, AutenticarForm
from django.contrib.auth import authenticate, login

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

# class InsertarUsuarioView(CreateView):
#     template_name = 'libreria/insertarUsuario.html'
#     form_class = UsuarioForm
#     queryset = Usuario.objects.all()    

#     def get_success_url(self):
#         return reverse("libreria:insertarUsuario")

#     def form_valid(self, form):          
#         return super().form_valid(form)

class AutenticarView(generic.FormView):
    template_name = 'libreria/autenticar.html'
    form_class = AutenticarForm

    def get_success_url(self):
        return reverse("libreria:librosAdmin")

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        usuario = authenticate(self.request, username = username, password = password)
        print(usuario)
        if usuario is not None:
            login(usuario)
            print('login')      
        return super(AutenticarView, self).form_valid(form)

class UserView(DetailView):
    template_name = 'libreria/profile.html'

    def get_object(self):
        return self.request.user


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(request, email=user.email, password=raw_password)
            if user is not None:
                login(request, user)
            else:
                print("user is not authenticated")
            return redirect('libreria:profile')
    else:
        form = SignUpForm()
    return render(request, 'users/registrarUsuario.html', {'form': form})

class LoginView(generic.FormView):
    template_name = 'libreria/login.html'
    form_class = AutenticarForm

    def get_success_url(self):
        return reverse("libreria:librosAdmin")

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        usuario = authenticate(self.request, username = username, password = password)
        if usuario is not None:
            login(self.request, usuario)
        else:
            return reverse("libreria:login")
        return super(LoginView, self).form_valid(form)

# Metodo par autenticar, en caso de error se mostraran un mensaje de error en la pagina de autenticacio,
# si las credenciales estan correctas se mostrara la pagina de listar libros

def autenticar(request):
    if request.method == 'POST':
        form = AutenticarForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('libreria:librosAdmin',))                
            else:
                form.add_error('username', 'incorrecto')
                form.add_error('password', 'incorrecto')
                messages.error(request, "Invalid username or password.")
                return render(request, 'libreria/autenticar.html', {'form':form})
       
    form = AutenticarForm()
    return render(request = request, template_name = "libreria/autenticar.html", context={"form":form})