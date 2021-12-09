from django.urls import path
from . import views

app_name = 'libreria'

urlpatterns = [
    path('', views.LibrosView.as_view(), name='libros'),   
    # path('', views.HomeView.as_view(), name='home'),    
]