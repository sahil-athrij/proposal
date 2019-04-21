from django.db import models
import os

# Create your models here.
def get_image_path(instance, filename):
    return os.path.join(str(instance.name), filename)

class person(models.Model):
    name = models.CharField(max_length=255)
    photo = models.FileField(upload_to=get_image_path)