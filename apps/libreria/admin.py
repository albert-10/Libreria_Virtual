from django.contrib import admin
from django.contrib.auth.models import Permission
from .models import Libro, Autor, Usuario, Review

# Registrando los modelos para acceder a ellos en el admin

admin.site.register(Libro)
admin.site.register(Autor)
admin.site.register(Usuario)
admin.site.register(Review)
admin.site.register(Permission)