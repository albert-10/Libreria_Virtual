from django.contrib import admin
from .models import Libro, Autor, Usuario, Review

admin.site.register(Libro)
admin.site.register(Autor)
admin.site.register(Usuario)
admin.site.register(Review)