from __future__ import unicode_literals
from django.db import models

# Nuestro administrador personalizado!
# Ningún método en nuestro nuevo administrador debería recibir el objeto de solicitud completo como argumento!
# (solo partes, como request.POST)
class ShowManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        # agregue claves y valores al diccionario de errores para cada campo no válido
        if len(postData['title']) < 3:
            errors["title"] = "El Titulo debe tener al menos 3 caracteres"
        if len(postData['new_network']) < 0:
            errors["new_network"] = "La Network debe tener al menos 3 caracteres"
        if len(postData['desc']) < 5:
            errors["desc"] = "La Descripcion debe tener al menos 5 caracteres"
        if len(postData['release_date']) < 3:
            errors["release_date"] = "La Fecha debe tener al menos 7 caracteres"
        return errors

class Channels(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Shows(models.Model):

    title = models.CharField(max_length=255)
    network = models.ForeignKey(Channels,related_name="shows",on_delete= models.CASCADE)
    desc = models.TextField()
    release_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ShowManager()

    def __repr__(self) -> str:
        return f'{self.title}: {self.network}: {self.desc}'