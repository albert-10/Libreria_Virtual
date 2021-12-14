from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import UserAdmin

from .models import Libro, Autor, Usuario, Review

admin.site.register(Libro)
admin.site.register(Autor)
admin.site.register(Usuario)
admin.site.register(Review)
admin.site.register(Permission)
