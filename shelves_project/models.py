from django.db import models
from django.contrib.auth.models import User


class Media(models.Model):
    mediaCode = models.CharField(max_length=5, unique=True)
    mediaCover = models.ImageField()
    mediaTitle = models.CharField(max_length=50)
    mediaCreator = models.CharField(max_length=250)
    mediaLanguage = models.CharField(max_length=50)
    mediaReleaseDate = models.DateField

    def __str__(self):
        return self.mediaCode



    # slightly different from ER diagram; added mediaCode, release date is a DateField


class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username

# Create your models here.
