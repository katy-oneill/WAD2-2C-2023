from django import forms
from shelves.models import Media, Book, Movie, Show, Song, Post, UserProfile
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator, int_list_validator
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

#------------------------------------------------------------------------------------------
class MediaForm(forms.ModelForm):
    title = forms.CharField(max_length=Media.TITLE_MAX_LENGTH,
                                help_text="Please enter the media title")
    
    type = forms.CharField(help_text="Please select the type of media",
                            widget=forms.Select(choices=Media.TYPE_CHOICES))

    writer = forms.CharField(max_length=Media.WRITER_MAX_LENGTH,
                                help_text="Please enter the media author")

    language = forms.CharField(max_length=Media.LANG_MAX_LENGTH,
                                help_text="Please enter the media language")
    
    releaseDate = forms.DateField(help_text="Please the enter release date")

    class Meta:
        model = Media
        fields = ('title', 'writer', 'language', 'releaseDate', 'type', )


class BookForm(forms.ModelForm):
        isbn = forms.CharField(max_length=Book.ISBN_MAX_LENGTH, 
                               help_text="The ISBN number must be 13 digits long")
        
        class Meta:
            model = Book
            fields = ('isbn', )


class MovieForm(forms.ModelForm):
        duration = forms.DurationField(help_text="Please enter the duration of the movie (H:MM:SS)")
        
        class Meta:
            model = Movie
            fields = ('duration', )


class ShowForm(forms.ModelForm):
        episodes = forms.IntegerField(help_text="Please enter the number of episodes")
        seasons = forms.IntegerField(help_text="Please enter the number of seasons")
        
        class Meta:
            model = Show
            fields = ('episodes', 'seasons' )


class SongForm(forms.ModelForm):
        duration = forms.DurationField(help_text="Please enter the duration of the song (H:MM:SS)")
        
        class Meta:
            model = Song
            fields = ('duration', )


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


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)
#------------------------------------------------------------------------------------------


class RegistrationForm(UserCreationForm):
    username = forms.CharField(label='Username', required=True)
    email = forms.EmailField(label='Email', required=True)
    first_name = forms.CharField(label='First Name', max_length=100)
    last_name = forms.CharField(label='Surname', max_length=100)
    age = forms.IntegerField(label='Age', min_value=13)
    gender_choices = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
    gender = forms.ChoiceField(label='Gender', choices=gender_choices)
    picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'age', 'gender', 'picture')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists.")
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Usename already taken.")
        return username

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.age = self.cleaned_data['age']
        user.gender = self.cleaned_data['gender']

        if commit:
            user.save()

        return user

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['age', 'picture']