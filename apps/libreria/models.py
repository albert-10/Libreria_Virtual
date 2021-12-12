import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.fields.related import ForeignKey
from django.shortcuts import reverse

User = get_user_model()

class Libro(models.Model):
    titulo = models.CharField(max_length=50)
    autor = models.ForeignKey('Autor', related_name='libros', on_delete=models.CASCADE)
    nombre_editorial = models.CharField(max_length=50)
    cantidad_paginas = models.PositiveIntegerField()
    fecha_publicacion = models.DateField()
    isbn = models.CharField(max_length=17)
    archivo_libro = models.FileField(upload_to='libros')

    class Meta:
        ordering = ["titulo"]

    def get_titulo(self):
        return self.titulo    

    def __str__(self):
        return self.get_titulo()   

    # Permite redirigira a la view editarLibro

    def get_absolute_url(self):
        return reverse("libreria:editarLibro", kwargs={'pk': self.id})

# Antes de eliminar el libro, se elimina el archivo del libro relacionado

    def delete(self, *args, **kwargs):
        self.archivo_libro.delete()
        super().delete(*args, **kwargs)

class Autor(models.Model):
    nombre = models.CharField(max_length=50)
    nacionalidad = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField()
    usuarios_suscritos = models.ManyToManyField(
        'Usuario',
        related_name='autores_suscritos',
        blank=True,
    )

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre

    # Retorna la cantidad de usuarios suscritos

    def cantidad_usuarios_suscritos(self):        
        return self.usuarios_suscritos.count()

    # Retorna los libros publicados

    def libros_publicados(self):        
        return self.libros.all()

    # Permite redirigira a la view editarAutor 

    def get_absolute_url(self):
        return reverse("libreria:editarAutor", kwargs={'pk': self.id})
        

class Usuario(models.Model):
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)    
    imagen = models.ImageField(upload_to='usuario_imagenes')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reviews = models.ManyToManyField(Libro, through='Review')
    fecha_registro = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.get_username()

    def get_username(self):
        return self.user.get_username()

    # Retorna la cantidad de autores a los que esta suscrito un usuario

    def cantidad_autores_suscritos(self):        
        return self.autores_suscritos.count()

class Review(models.Model):
    CALIFICACION = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )

    usuario = ForeignKey(Usuario, on_delete=models.CASCADE)
    libro = ForeignKey(Libro, on_delete=models.CASCADE)
    fecha_creada = models.DateTimeField(auto_now_add=True)
    opinion = models.TextField()
    calificacion = models.IntegerField(choices=CALIFICACION)

    def __str__(self):
        return f"{self.usuario.get_username()} - {self.libro.get_titulo()} - {self.calificacion}"

