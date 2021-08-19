from django.db import models

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

    def __repr__(self) -> str:
        return f'{self.title}: {self.network}: {self.desc}'