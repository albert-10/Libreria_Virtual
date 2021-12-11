from django.urls import path
from . import views

app_name = 'libreria'

urlpatterns = [
    path('', views.LibrosView.as_view(), name='libros'),   
    path('insertarLibro/', views.InsertarLibroView.as_view(), name='insertarLibro'),
    path('editarLibro/<pk>/', views.EditarLibroView.as_view(), name='editarLibro'),
    path('eliminarLibro/<pk>/', views.EliminarLibroView.as_view(), name='eliminarLibro'),
    path('librosAdmin/', views.LibrosAdminView.as_view(), name='librosAdmin'),   

    path('insertarAutor/', views.InsertarAutorView.as_view(), name='insertarAutor'), 
]