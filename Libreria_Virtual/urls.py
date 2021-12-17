
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('libreria.urls'), name='libreria'),
]

# Permite mostrar la pagina de mensaje de error cuando la pagina no ha sido encontrada

def error_404(request, exception):       
    return render(request,'paginaNoEncontrada.html')

handler404 = error_404

