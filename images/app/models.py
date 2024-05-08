from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)


class ImageLike(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT)


class Image(models.Model):
    name = models.CharField(max_length=255)
    file = models.ImageField(upload_to="images")
    created_at = models.DateTimeField(auto_created=True)
    likes = models.ManyToManyField(ImageLike)
