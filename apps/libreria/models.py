import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.fields.related import ForeignKey
from django.shortcuts import reverse

User = get_user_model()

class Libro(models.Model):
    titulo = models.CharField(max_length=50)
    autor = models.ForeignKey('Autor', on_delete=models.CASCADE)
    nombre_editorial = models.CharField(max_length=50)
    cantidad_paginas = models.PositiveIntegerField()
    fecha_publicacion = models.DateField()
    isbn = models.CharField(max_length=17)
    archivo_libro = models.FileField(upload_to='libros')

    def get_titulo(self):
        return self.titulo    

    def __str__(self):
        return self.get_titulo()   

    def get_absolute_url(self):
        return reverse("libreria:editarLibro", kwargs={'pk': self.id})

class Autor(models.Model):
    nombre = models.CharField(max_length=50)
    nacionalidad = models.CharField(max_length=20)
    fucha_nacimiento = models.DateField()

    def __str__(self):
        return self.nombre

class Usuario(models.Model):
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)    
    imagen = models.ImageField(upload_to='usuario_imagenes')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reviews = models.ManyToManyField(Libro, through='Review')

    def __str__(self):
        return self.get_username()

    def get_username(self):
        return self.user.get_username()

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

