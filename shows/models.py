from __future__ import unicode_literals
from django.db import models

# Nuestro administrador personalizado!
# Ningún método en nuestro nuevo administrador debería recibir el objeto de solicitud completo como argumento!
# (solo partes, como request.POST)

class UsersManager(models.Manager):

    def basic_validator(self,postData):
        errors={}

        if len(postData['name']) < 4:
            errors['name'] = "El nombre de usuario debe tener al menos 3 letras"

        if len(postData['email']) < 4:
            errors['email'] = "El email de usuario debe tener al menos 4 letras"

        if len(postData['password']) < 6:
            errors['password'] = "La contraseña de usuario debe tener al menos 6 caracteres"

        if postData['password'] != postData['password_confirm']:
            errors['password'] = "Ambas contraseñas deben ser iguales"


        return errors

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

'''
class WizardsManager(models.Manager):
    
    def basic_validator(self, postData):
        errors = {}

        if len(postData['name']) < 4:
            errors["name"] = "El nombre del Mago debe tener al menos 4 letras"
        
        if len(postData['house_id']) < 1:
            errors["house_id"] = "Debe seleccionar al menos 1 casa"
        
        if len(postData['pet']) < 4:
            errors["pet"] = "El nombre de la Mascota debe tener al menos 4 letras"
        
        try:
            year = int(postData['year'])
            if year < 1:
                errors['year'] = "El año debe ser al menos 1"

        except ValueError:
            errors["year"] = "El campo 'Año' debe ser un número"
        
        return errors
'''

class Users(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    allowed = models.BooleanField(default=True)
    avatar = models.URLField(
        default = "https://png.pngtree.com/png-vector/20191026/ourlarge/pngtree-avatar-vector-icon-white-background-png-image_1870181.jpg"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UsersManager()

    def __repr__(self) -> str:
        return f'{self.name}: {self.email}'

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