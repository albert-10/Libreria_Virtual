from django.urls import path
from . import views

app_name = 'libreria'

urlpatterns = [
    path('', views.LibrosView.as_view(), name='libros'),   
    path('insertarLibro/', views.InsertarLibroView.as_view(), name='insertarLibro'),
    path('librosAdmin/', views.LibrosAdminView.as_view(), name='librosAdmin'),    
]