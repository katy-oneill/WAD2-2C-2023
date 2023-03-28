from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from shelves.models import Media, Book, Movie, Show, Song, Post, UserProfile, Friendship
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator, int_list_validator


class MediaForm(forms.ModelForm):

    media_type = forms.CharField(help_text="Please select the type of media you wish to store",
                            widget=forms.Select(choices=Media.TYPE_CHOICES))

    class Meta:
        model = Media
        fields = ('media_type', )


class BookForm(forms.Form):

        title = forms.CharField(max_length = Media.TITLE_MAX_LENGTH, help_text= "Title of the book")

        author = forms.CharField(max_length = Media.WRITER_MAX_LENGTH, help_text= "Name of the book's author")

        language = forms.CharField(help_text="What language is the book primarily written in?")

        isbn = forms.CharField(max_length=Book.ISBN_MAX_LENGTH, help_text="The ISBN number must be 13 digits long")

        numberOfPages = forms.CharField(help_text="How many pages does the book have?")
        
        
        class Meta:
            model = Book
            fields = ('isbn', 'title', 'author', 'language','numberOfPages',)


class MovieForm(forms.ModelForm):
        title = forms.CharField(max_length = Media.TITLE_MAX_LENGTH, help_text= "Title of the movie")

        duration = forms.DurationField(help_text="Please enter the duration of the movie")

        language = forms.CharField(help_text="What language is the movie primarily in?")

        mainCast = forms.CharField(help_text="Who are the main cast of the movie?")

        director = forms.CharField(help_text="Who is the director of the movie?")
        
        class Meta:
            model = Movie
            fields = ('title','duration','language', 'mainCast', 'director', )


class ShowForm(forms.ModelForm):

        title = forms.CharField(max_length = Media.TITLE_MAX_LENGTH, help_text= "Title of the show")

        episodes = forms.IntegerField(help_text="Please enter the number of episodes")

        seasons = forms.IntegerField(help_text="Please enter the number of seasons")

        language = forms.CharField(help_text="What language is the show primarily in?")

        mainCast = forms.CharField(help_text="Who are the main cast of the show?")

        director = forms.CharField(help_text="Who is the director of the show?")

        channel = forms.CharField(help_text="What channel does the show air on?")
        
        class Meta:
            model = Show
            fields = ('title','episodes', 'seasons', 'language', 'mainCast', 'director', 'channel', )


class SongForm(forms.ModelForm):

        title = forms.CharField(max_length = Media.TITLE_MAX_LENGTH, help_text= "Title of the song")

        duration = forms.DurationField(help_text="Please enter the duration of the song")

        language = forms.CharField(help_text="What language is the song primarily in?")

        artist = forms.CharField(help_text="The song is by which artist")

        Platforms = forms.CharField(help_text="What platforms are you aware of where this song is available?")

        class Meta:
            model = Song
            fields = ('title','duration', 'language', 'artist', 'Platforms')


class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=Post.TITLE_MAX_LENGTH,
                                    help_text="Enter the title of your post")
    
    rating = forms.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)],
                                    help_text="Provide a score between 0 and 10")
    
    comment = forms.CharField(widget=forms.Textarea, max_length=Post.COMM_MAX_LENGTH,
                                    help_text="Enter your comment")
    
    class Meta:
        model = Post
        fields = ['title', 'rating', 'comment',]


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(label='Email', required=True)
    first_name = forms.CharField(label='First Name', max_length=100)
    last_name = forms.CharField(label='Surname', max_length=100)
    age = forms.IntegerField(label='Age', min_value=13)
    gender_choices = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
    gender = forms.ChoiceField(label='Gender', choices=gender_choices)
    picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2', 'age', 'gender', 'picture')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(username=email).exists():
            raise ValidationError("Email already exists.")
        return email

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.username = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.age = self.cleaned_data['age']
        user.gender = self.cleaned_data['gender']

        if commit:
            user.save()

        return user

class FriendshipForm(forms.ModelForm):
    username = forms.CharField(label='Email', required=True)
    class Meta:
        model = Friendship
        fields = []

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['age', 'picture']

