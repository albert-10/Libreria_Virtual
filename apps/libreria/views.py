import os
from django.core.mail import send_mail
from django.shortcuts import redirect, reverse, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Permission,User
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views import generic
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.views.generic.detail import DetailView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import  UpdateView, DeleteView, CreateView
from django.conf import settings
from .filters import Libro_Filter, Autor_Filter, Usuario_Filter, Review_Filter, Review_Libro_Filter
from .models import Libro, Autor, Review, Usuario
from .forms import LibroForm, AutorForm, AutenticarForm, UsuarioForm, RegistrarForm, ReviewForm
from django.contrib.auth.decorators import permission_required, login_required

# La siguiente vista retorna libros segun el filtro que realice el usuario

class ListarLibrosView(generic.ListView):
    model = Libro
    template_name = 'libreria/listarLibros.html'

    # El siguiente metodo permite obtener una page de libro, de acuerdo al filtro
    # de libros que se haya aplicado.

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

class InsertarLibroView(PermissionRequiredMixin, generic.FormView):
    template_name = 'libreria/insertarLibro.html'
    form_class = LibroForm
    permission_required = 'libreria.administrador'
    raise_exception = True

    def get_success_url(self):
        return reverse("libreria:insertarLibro")

    # El siguiente metodo una vez que el formulario este correcto, envia un email a los usuarios suscritos
    # al autor del libro, informandole del nuevo libro publicado por el autor

    def form_valid(self, form):
        nombre_autor = form.cleaned_data['autor'].nombre
        titulo_libro = form.cleaned_data['titulo']
        lista_email_usuarios_suscritos = form.cleaned_data['autor'].get_emails_usuarios_suscritos()
        if len(lista_email_usuarios_suscritos) > 0:            
            mensaje = f"""
                Estimado lector, el autor: {nombre_autor}, ha publicado su nuevo libro: {titulo_libro}                
            """
            send_mail(
                subject=str(settings.ASUNTO_EMAIL),
                message=mensaje,
                from_email=str(settings.DEFAULT_FROM_EMAIL),
                recipient_list=lista_email_usuarios_suscritos
            )
        messages.success(self.request, "Libro insertado correctamente")
        form.save(commit=True)
        return super(InsertarLibroView, self).form_valid(form)

    # Permitira mostrar un mensaje de error cuando los campos del formulario sean invalidos

    def form_invalid(self, form):
        messages.error(self.request, "Campos no v??lidos")
        return render(self.request, 'libreria/insertarLibro.html', {'form':form})        

# La siguiente clase permite editar Libros

class EditarLibroView(PermissionRequiredMixin, UpdateView):
    template_name = 'libreria/editarLibro.html'
    model = Libro
    form_class = LibroForm    
    permission_required = 'libreria.administrador'
    raise_exception = True
    
    def get_object(self):
        return get_object_or_404(Libro, pk=self.kwargs["pk"])

    # Antes de editar el libro se comprueba que en el formulario haya un nuevo archivo. Si es asi se elimina
    # el antiguo archivo antes de guardar la edicion del libro

    def form_valid(self, form):
        if len(self.request.FILES) > 0:
            libro = self.get_object()
            os.remove(libro.archivo_libro.path)
        messages.success(self.request, "Libro editado correctamente")
        form.save(commit=True)
        return super().form_valid(form)

    # Permitira mostrar un mensaje de error cuando los campos del formulario sean invalidos

    def form_invalid(self, form):
        messages.error(self.request, "Campos no v??lidos")
        return render(self.request, 'libreria/editarLibro.html', {'form':form}) 

# La siguiente clase permite eliminar Libros

class EliminarLibroView(PermissionRequiredMixin, DeleteView):    
    model = Libro
    success_url = reverse_lazy('libreria:listarLibros')
    permission_required = 'libreria.administrador'
    raise_exception = True

# La siguiente vista pemite insertar autores

class InsertarAutorView(PermissionRequiredMixin, CreateView):
    template_name = 'libreria/insertarAutor.html'
    form_class = AutorForm
    queryset = Autor.objects.all()
    permission_required = 'libreria.administrador'
    raise_exception = True

    def get_success_url(self):
        return reverse("libreria:insertarAutor")

    # Permitira mostrar un mensaje de exito cuando se inserte correctamente un Autor

    def form_valid(self, form):
        messages.success(self.request, "Autor insertado correctamente")    
        return super().form_valid(form)

    # Permitira mostrar un mensaje de error cuando los campos del formulario sean invalidos

    def form_invalid(self, form):
        messages.error(self.request, "Campos no v??lidos")
        return render(self.request, 'libreria/insertarAutor.html', {'form':form})

# la siguiente clase permite listar autores

class ListarAutoresView(generic.ListView):
    model = Autor
    template_name = 'libreria/listarAutores.html'

    # El siguiente metodo permite obtener una pagina con Autores, de acuerdo al filtro
    # de autores que se haya aplicado.

    def get_context_data(self, **kwargs):             
        context = super().get_context_data(**kwargs)        
        autor_filter = Autor_Filter(self.request.GET, queryset=self.get_queryset())
        context['autor_filter'] = autor_filter
        autores_filtrados_paginados = Paginator(autor_filter.qs, 5)      
        numero_de_pagina = self.request.GET.get('page')

        autor_page = autores_filtrados_paginados.get_page(numero_de_pagina)
        context['autor_page'] = autor_page
        return context

# La siguiente clase permitira mostrar los detalles de un autor

class DetallesAutorView(generic.DetailView):
    template_name = 'libreria/detallesAutor.html'
    queryset = Autor.objects.all()
    context_object_name = 'autor'

# La siguiente clase permite eliminar autores

class EliminarAutorView(PermissionRequiredMixin, DeleteView):    
    model = Autor
    success_url = reverse_lazy('libreria:listarAutores')
    permission_required = 'libreria.administrador'
    raise_exception = True

# La siguiente clase permite editar autores

class EditarAutorView(PermissionRequiredMixin, UpdateView):
    template_name = 'libreria/editarAutor.html'
    form_class = AutorForm
    model = Autor
    permission_required = 'libreria.administrador'
    raise_exception = True
    
    def get_object(self):
        return get_object_or_404(Autor, pk=self.kwargs["pk"])
    
    # Permitira mostrar un mensaje de exito cuando se edite correctamente un Autor

    def form_valid(self, form):
        messages.success(self.request, "Autor editado correctamente")
        form.save(commit=True)
        return super().form_valid(form)

    # Permitira mostrar un mensaje de error cuando los campos del formulario sean invalidos

    def form_invalid(self, form):
        messages.error(self.request, "Campos no v??lidos")
        return render(self.request, 'libreria/editarAutor.html', {'form':form})

# La siguiente clase permite listar usuarios, tambien filtrarlos y paginarlos

class ListarUsuariosView(PermissionRequiredMixin, generic.ListView):
    model = Usuario
    template_name = 'libreria/listarUsuarios.html'
    permission_required = 'libreria.administrador'
    raise_exception = True   

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)       
        usuario_filter = Usuario_Filter(self.request.GET, queryset=self.get_queryset())
        context['usuario_filter'] = usuario_filter
        usuarios_filtrados_paginados = Paginator(usuario_filter.qs, 5)
       
        numero_de_pagina = self.request.GET.get('page')
        usuario_page = usuarios_filtrados_paginados.get_page(numero_de_pagina)
        cantidad_usuarios = Usuario.objects.all().count()
        context['usuario_page'] = usuario_page
        context['cantidad_usuarios'] = cantidad_usuarios
        return context

# El siguiente metodo permite insertar un usuario y asignarle permiso de administrador,
# en caso de que tenga ese valor en el formulario

@permission_required('libreria.administrador', raise_exception=True)
def insertar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data.get('username')            
            email = form.cleaned_data.get('email')
            first_name = form.cleaned_data.get('first_name')
            password = form.cleaned_data.get('password')
            imagen = form.cleaned_data.get('imagen')
            es_Administrador = form.cleaned_data.get('is_admin')            
            User = get_user_model()
            user, es_usuario_creado = User.objects.get_or_create(
                username=username,
                defaults={'username':username, 'email':email, 'first_name':first_name},
            )
            if es_usuario_creado:
                if es_Administrador:
                    permission = Permission.objects.get(codename='administrador')
                    user.user_permissions.add(permission)
                user.set_password(password)
                user.save() 
                Usuario.objects.create(imagen=imagen, user=user)
                messages.success(request, "Usuario insertado correctamente")
                return HttpResponseRedirect(reverse('libreria:insertarUsuario',))            
            else:
                messages.error(request, "Los campos no son v??lidos")
                form.add_error('username', 'El username ya existe')
                return render(request, 'libreria/insertarUsuario.html', {'form':form})
        else:
            messages.error(request, "Los campos no son v??lidos")
            return render(request = request, template_name = "libreria/insertarUsuario.html", context={"form":form})       
    form = UsuarioForm()
    return render(request = request, template_name = "libreria/insertarUsuario.html", context={"form":form})

# El siguiente metodo permite editar un usuario y asignarle permiso de administrador,
# en caso de que tenga ese valor en el formulario

@permission_required('libreria.administrador', raise_exception=True)
def editar_usuario(request, guid):   
    usuario = get_object_or_404(Usuario, guid=guid)
    guid_usuario = usuario.guid
    user = usuario.user
    if request.method == 'POST':
        form = UsuarioForm(request.POST, request.FILES)
        if form.is_valid():            
            username = form.cleaned_data.get('username')            
            User = get_user_model()
            username_usado = User.objects.filter(~Q(id=user.pk) & Q(username=username)).exists()
            if not username_usado:
                username = form.cleaned_data.get('username')            
                email = form.cleaned_data.get('email')
                first_name = form.cleaned_data.get('first_name')
                password = form.cleaned_data.get('password')
                imagen = form.cleaned_data.get('imagen')

                # Eliminando antigua imagen
                
                if not usuario.imagen == '':
                    os.remove(usuario.imagen.path)               
                es_Administrador = form.cleaned_data.get('is_admin')                
                usuario.imagen = imagen
                usuario.save()
                user.username = username
                user.email = email
                user.first_name = first_name
                user.set_password(password)                  
                if es_Administrador:
                    permission = Permission.objects.get(codename='administrador')
                    user.user_permissions.add(permission)
                else:
                    user.user_permissions.clear()
                user.save()

                # Cuando el usuario se esta editando a si mismo, se autenticara otra vez. En caso que no se edite como
                # Administrador se redirigira a la pagina listarLibros

                if user.id == request.user.id:
                    userAutenticar = authenticate(username=username, password=password)
                    login(request, userAutenticar)
                    if not es_Administrador:
                        return HttpResponseRedirect(reverse('libreria:listarLibros'))               
                messages.success(request, "Usuario Editado correctamente")
                return HttpResponseRedirect(reverse('libreria:editarUsuario', args=(guid_usuario,)) )
            else:
                messages.error(request, "El username ya existe")
                form.add_error('username', 'El username ya existe')
                return render(request, 'libreria/editarUsuario.html', {'form':form, 'guid_usuario': guid_usuario})
        else:
            messages.error(request, "Los campos no son v??lidos")
            return render(request = request, template_name = "libreria/editarUsuario.html", context={"form":form, 'guid_usuario': guid_usuario})     
    usuario_es_administrador = len(user.get_user_permissions()) > 0
    
    datos = {'first_name': user.first_name, 'username': user.username, 'email': user.email, 'is_admin': usuario_es_administrador}
    form = UsuarioForm(datos)    
    return render(request = request, template_name = "libreria/editarUsuario.html", context={"form":form, 'guid_usuario': guid_usuario})

# La siguiente view permite que un usuario se registre

def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistrarForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data.get('username')            
            email = form.cleaned_data.get('email')
            first_name = form.cleaned_data.get('first_name')
            password = form.cleaned_data.get('password')
            imagen = form.cleaned_data.get('imagen')
            User = get_user_model()
            user, es_usuario_creado = User.objects.get_or_create(
                username=username,
                defaults={'username':username, 'email':email, 'first_name':first_name},
            )
            if es_usuario_creado:
                user.set_password(password)
                user.save() 
                Usuario.objects.create(imagen=imagen, user=user)
                login(request, user)             
                return HttpResponseRedirect(reverse('libreria:listarLibros',))            
            else:
                messages.error(request, "Los campos no son v??lidos")
                form.add_error('username', 'El username ya existe')
                return render(request, 'libreria/registrarUsuario.html', {'form':form})
        else:
            messages.error(request, "Los campos no son v??lidos")
            return render(request = request, template_name = "libreria/registrarUsuario.html", context={"form":form})  
    form = RegistrarForm()
    return render(request = request, template_name = "libreria/registrarUsuario.html", context={"form":form})

# El siguiente metodo permite autenticar un usuario

def autenticar(request):
    if request.method == 'POST':
        form = AutenticarForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('libreria:listarLibros',))                
            else:
                form.add_error('username', 'incorrecto')
                form.add_error('password', 'incorrecto')
                messages.error(request, "Invalid username or password.")
                return render(request, 'libreria/autenticar.html', {'form':form})       
    form = AutenticarForm()
    return render(request = request, template_name = "libreria/autenticar.html", context={"form":form})

# El siguiente metodo permite a un usuario salir de sesion

def salir_sesion(request):
    logout(request)
    return redirect('libreria:listarLibros')

# La siguiente clase permite eliminar Libros

class EliminarUsuarioView(PermissionRequiredMixin, DeleteView):  
    model = User
    success_url = reverse_lazy('libreria:listarUsuarios')
    permission_required = 'libreria.administrador'
    raise_exception = True

    # El siguiente metodo permite eliminar la imagen del usuario, si este tiene. En caso
    # de que el usuario se elimine a si mismo, se mostrara la pagina donde se muestran los libros

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        usuario = self.object.usuario
        if not usuario.imagen == '':
            os.remove(usuario.imagen.path)
        if usuario.user == request.user:
            self.object.delete()
            return HttpResponseRedirect(reverse('libreria:listarLibros',))        
        self.object.delete()
        return HttpResponseRedirect(self.success_url)

# El siguiente metodo permite que un usuario se suscriba a un autor

@login_required()
def suscribirse_a_autor(request, pk):
    user = User.objects.get(pk=request.user.pk)
    usuario = user.usuario
    autor = get_object_or_404(Autor, pk=pk)
    autor.usuarios_suscritos.add(usuario)
    return HttpResponseRedirect(reverse('libreria:listarAutores'))

# El siguiente metodo anula la suscripcion de un usuario a un autor

@login_required()
def eliminar_suscripcion_autor(request, pk):
    user = User.objects.get(pk=request.user.pk)
    usuario = user.usuario
    autor = get_object_or_404(Autor, pk=pk)
    autor.usuarios_suscritos.remove(usuario)
    return HttpResponseRedirect(reverse('libreria:listarAutores'))

# El siguiente funcion permite crear una review

@login_required()
def insertar_review(request, guid, pk):
    libro = get_object_or_404(Libro, id=pk) 
    if request.method == 'POST':
        usuario = get_object_or_404(Usuario, guid=guid)               
        form = ReviewForm(request.POST)
        if form.is_valid():
            opinion = form.cleaned_data.get('opinion') 
            calificacion = form.cleaned_data.get('calificacion')                     
            Review.objects.create(usuario=usuario, libro=libro, opinion=opinion, calificacion=calificacion)
            messages.success(request, "Review creada correctamente")
            return HttpResponseRedirect(reverse('libreria:insertarReview', args=(guid, pk)))
        else:
            messages.error(request, "Campo incorrecto")
            return render(request, 'libreria/insertarReview.html', {'form':form, 'guid': guid, 'pk': pk, 'libro_titulo': libro.titulo})
    else:        
        form = ReviewForm()
        return render(request = request, template_name = "libreria/insertarReview.html", context={'form':form ,'libro_titulo': libro.titulo})

# La siguiente clase permite listar las reviews

class ListarReviewsView(generic.ListView):
    model = Review
    template_name = 'libreria/listarReviews.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        review_filter = Review_Filter(self.request.GET, queryset=self.get_queryset())
        context['review_filter'] = review_filter
        reviews_filtradas_paginadas = Paginator(review_filter.qs, 5)           
        numero_de_pagina = self.request.GET.get('page')
        review_page = reviews_filtradas_paginadas.get_page(numero_de_pagina)        
        context['review_page'] = review_page
        return context

# La siguiente vista permite mostrar las reviews de un libro

class ListarReviewsLibroView(DetailView):    
    model = Libro
    template_name = 'libreria/listarReviewsLibro.html'

    def get_context_data(self, **kwargs):       
        context = super().get_context_data(**kwargs)
        review_libro_filter = Review_Libro_Filter(self.request.GET, queryset=Review.objects.filter(libro=context['libro']))
        context['review_libro_filter'] = review_libro_filter
        reviews_filtradas_paginadas = Paginator(review_libro_filter.qs, 5)
        numero_de_pagina = self.request.GET.get('page')
        review_page = reviews_filtradas_paginadas.get_page(numero_de_pagina)  
        context['review_libro_filter_page'] = review_page
        return context

# La siguiente clase permite eliminar una review

class EliminarReviewView(PermissionRequiredMixin, DeleteView):    
    model = Review
    success_url = reverse_lazy('libreria:listarReviews')
    permission_required = 'libreria.administrador'
    raise_exception = True