import datetime
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator, int_list_validator


class Media(models.Model):
    # Max-length values
    TITLE_MAX_LENGTH = 50
    WRITER_MAX_LENGTH = 50
    LANG_MAX_LENGTH = 50
    
    # Fields
    title = models.CharField(max_length=TITLE_MAX_LENGTH, unique=True)
    mediaCoverImage = models.ImageField(blank=True)
    writer = models.CharField(max_length=WRITER_MAX_LENGTH)
    language = models.CharField(max_length=LANG_MAX_LENGTH)
    publishDate = models.DateField(blank=True)
    avgScore = models.FloatField(default=0)

    # Slug
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Media, self).save(*args, **kwargs)
    
    # Keep track of avg. rating for media
    def updateAvgScore(self, media):
        posts = media.post_set.all()
        numberOfPosts = len(posts)

        if (numberOfPosts != 0):
            scoreSum = 0

            for post in posts:
                scoreSum += post.rating
            
            self.avgScore = scoreSum/numberOfPosts
            self.save()

    # To string
    def __str__(self):
        return self.title
    

class Book(models.Model):
    # FK
    media = models.OneToOneField(Media, on_delete=models.CASCADE)

    # Max Length Values
    ISBN_MAX_LENGTH = 13

    # Fields
    isbn = models.CharField(max_length=ISBN_MAX_LENGTH, validators=[MinLengthValidator(13), int_list_validator(sep='')])


class Movie(models.Model):
    # FK
    media = models.OneToOneField(Media, on_delete=models.CASCADE)
    
    # Max Length Values
    LOC_MAX_LENGTH = 50

    # Fields
    location = models.CharField(max_length=LOC_MAX_LENGTH)
    duration = models.DurationField(default=datetime.timedelta())


class Show(models.Model):
    # FK
    media = models.OneToOneField(Media, on_delete=models.CASCADE)

    # Fields
    episodes = models.IntegerField(default=0)
    seasons = models.IntegerField(default=0)


class Song(models.Model):
    # FK
    media = models.OneToOneField(Media, on_delete=models.CASCADE)

    # Fields
    duration = models.DurationField(default=datetime.timedelta())


class Post(models.Model):
    # FK
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Max Length Values
    TITLE_MAX_LENGTH = 50
    COMM_MAX_LENGTH = 1000

    # Attributes
    title = models.CharField(max_length=TITLE_MAX_LENGTH)
    rating = models.IntegerField(default=0,validators=[MinValueValidator(0), MaxValueValidator(10)])
    comment = models.TextField(max_length=COMM_MAX_LENGTH, blank=True)
    publishDate = models.DateField(default=datetime.date.today)
    likes = models.IntegerField(default=0)

    # Slug
    slug = models.SlugField(unique=True)

    # Links user and media so that a user cannot have more than 1 post per media
    class Meta:
        unique_together = ('media','user')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Media, self).save(*args, **kwargs)
        self.media.updateScore(media=self.media)
    
    # To string
    def __str__(self):
        return self.title
    

class UserProfile(models.Model):
    # FK
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Attributes
    picture = models.ImageField(blank=True)
    age = models.IntegerField(validators=[MinValueValidator(13)])
    joinDate = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.user.username
