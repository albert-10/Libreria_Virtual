from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'libreria'

urlpatterns = [

    path('autenticar/', views.autenticar, name='autenticar'),
    path('salirSesion/', views.salir_sesion, name='salirSesion'),    

    # path('', views.LibrosView.as_view(), name='libros'),  
    path('', views.LibrosAdminView.as_view(), name='librosAdmin'), 
    path('insertarLibro/', views.InsertarLibroView.as_view(), name='insertarLibro'),
    path('editarLibro/<pk>/', views.EditarLibroView.as_view(), name='editarLibro'),
    path('eliminarLibro/<pk>/', views.EliminarLibroView.as_view(), name='eliminarLibro'),
    #path('librosAdmin/', views.LibrosAdminView.as_view(), name='librosAdmin'),   

    path('insertarAutor/', views.InsertarAutorView.as_view(), name='insertarAutor'),
    path('listarAutores/', views.ListarAutoresView.as_view(), name='listarAutores'),
    path('detallesAutor/<pk>/', views.DetallesAutorView.as_view(), name='detallesAutor'),
    path('editarAutor/<pk>/', views.EditarAutorView.as_view(), name='editarAutor'),
    path('eliminarAutor/<pk>/', views.EliminarAutorView.as_view(), name='eliminarAutor'),

    path('listarUsuarios/', views.ListarUsuariosView.as_view(), name='listarUsuarios'),
    path('insertarUsuario/', views.insertar_usuario, name='insertarUsuario'),
    path('editarUsuario/<uuid:guid>/', views.editar_usuario, name='editarUsuario'),
    path('eliminarUsuario/<pk>/', views.EliminarUsuarioView.as_view(), name='eliminarUsuario'),

    path('suscribirseAAutor/<pk>/', views.suscribirse_a_autor, name='suscribirseAAutor'),
    path('eliminarSuscripcionAutor/<pk>/', views.eliminar_suscripcion_autor, name='eliminarSuscripcionAutor'),

    path('insertarReview/<uuid:guid>/<pk>/', views.insertar_review, name='insertarReview'),
    path('listarReviews/', views.ListarReviewsView.as_view(), name='listarReviews'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)