from django.shortcuts import render
from django.views import generic
from .models import Libro

""" class Home(generic.TemplateView):
    template_name = 'libreria/home.html' """

class HomeView(generic.ListView):
    template_name='libreria/home.html'
    queryset = Libro.objects.all()