from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

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
