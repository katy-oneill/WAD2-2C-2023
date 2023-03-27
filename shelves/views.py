from django.shortcuts import render, redirect
from django.http import HttpResponse
from shelves.form import ProfileUpdateForm, RegistrationForm, MediaForm, BookForm, MovieForm, ShowForm, SongForm, PostForm, FriendshipForm
from django.contrib.auth import login, logout
from shelves.models import Media, Book, Movie, Show, Song, Post, UserProfile, Friendship
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.models import User

def launch(request):
    if request.user.is_authenticated:
        return render(request, 'shelves/dashboard.html')
    else:
        return render(request, 'shelves/launch.html')

def friends(request):
    return render(request, 'shelves/friends.html')

def social(request):
    return render(request, 'shelves/social.html')

def login_view(request):
    return render(request, 'shelves/login.html')

def logout_view(request):
    logout(request)
    return redirect('launch')

def books(request):
    return render(request, 'shelves/books.html')

def albums(request):
    return render(request, 'shelves/albums.html')

def shows(request):
    return render(request, 'shelves/shows.html')

def movies(request):
    return render(request, 'shelves/movies.html')

@login_required
def view_profile(request):
    user = request.user
    profile = UserProfile.objects.get_or_create(user=user)[0]
    context = {'user': user, 'profile': profile}
    return render(request, 'shelves/view_profile.html', context)

@login_required
def edit_profile(request):
    user = request.user
    profile = UserProfile.objects.get(user=user)
    profile_form = ProfileUpdateForm(instance=profile)

    if request.method == 'POST':
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect(reverse('shelves:view_profile'))

    context = {'user': user, 'profile_form': profile_form}
    return render(request, 'shelves/edit_profile.html', context)


# Add media -> redirect user to submit extra information
# pertinent to the specific type of media they've added.
# E.g., if they add a book, redirect them to the page that
# asks for the ISBN number.
@login_required
def add_media(request):
    media_form = MediaForm()

    if request.method == 'POST':
        media_form = MediaForm(request.POST)

        if media_form.is_valid():
            media = media_form.save(commit=False)
            media.user = request.user
            media.save()
            return redirect(reverse('add_type_details', kwargs={'media_title_slug': media.slug}))

        else:
            print(media_form.errors)

    return render(request, 'shelves/add_media.html', {'form': media_form})


@login_required
def add_type_details(request, media_title_slug):
    try:
        media = Media.objects.get(slug=media_title_slug)
    except Media.DoesNotExist:
        media = None

    if media is None:
        return redirect(reverse('add_media'))
    
    if media.type == "book":
        type_form = BookForm
    elif media.type == 'movie':
        type_form = MovieForm
    elif media.type == 'show':
        type_form = ShowForm
    elif media.type == 'song':
        type_form = SongForm

    if request.method == 'POST':
        type_form = type_form(request.POST)

        if type_form.is_valid():
            type = type_form.save(commit=False)
            type.media = media
            type.save()

            return redirect(reverse('show_media',
                                    kwargs={'media_title_slug':
                                            media_title_slug,
                                            'media_type':
                                            media.type}))
        else:
            print(type_form.errors)

    context_dict = {'form': type_form, 'media': media}
    return render(request, 'shelves/add_type_details.html', context=context_dict)


@login_required
def add_post(request, media_title_slug):
    try:
        media = Media.objects.get(slug=media_title_slug)
    except Media.DoesNotExist:
        media = None

    if media is None:
        return redirect('/shelves/')

    post_form = PostForm()

    if request.method == 'POST':
        post_form = PostForm(request.POST)

        if post_form.is_valid():
            if media:
                post = post_form.save(commit=False)
                post.media = media
                post.likes = 0
                post.user = request.user
                post.save()

                return redirect(reverse('show_media',
                                        kwargs={'media_title_slug':
                                                media_title_slug}))
        else:
            print(post_form.errors)

    context_dict = {'form': post_form, 'media': media}
    return render(request, 'shelves/add_post.html', context=context_dict)

def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            picture = form.cleaned_data.get('picture')
            age = form.cleaned_data.get('age')
            UserProfile.objects.create(user=user, age=age)
            login(request, user)
            return redirect('registration_success')
    else:
        form = RegistrationForm()
    return render(request, 'shelves/register.html', {'form': form})

def registration_success(request):
    user_profile = request.user.userprofile
    return render(request, 'shelves/dashboard.html', {'user_profile': user_profile})

# @login_required
def dashboard(request):
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = None
    return render(request, 'shelves/dashboard.html', {'user_profile': user_profile})

def social(request):

    if request.method == 'POST':
        form = FriendshipForm(request.POST)
        if form.is_valid():
            friendship = form.save(commit=False)
            friendship.follower = request.user
            friendship.save()
            return redirect('social')
    else:
        form = FriendshipForm()
    return render(request, 'shelves/social.html', {'form': form})

#def social(request):
 #   return 0


@login_required
def send_friend_request(request, username):
    sender = request.user
    receiver = User.objects.get(username=username)
    
    Friendship.objects.get_or_create(sender=sender, receiver=receiver)
    return redirect(reverse('view_profile', kwargs={'username':username}))


@login_required
def accept_friend_request(request, username):
    receiver = request.user
    sender = User.objects.get(username=username)

    try:
        friend_request = Friendship.objects.get(sender=sender, receiver=receiver)
    except:
        friend_request = None

    if friend_request != None:
        receiver = UserProfile.objects.get(user=receiver)
        sender = UserProfile.objects.get(user=sender)
        
        sender.friends.add(receiver)
        receiver.friends.add(sender)
        friend_request.delete()
    
    return redirect(reverse('view_profile', kwargs={'username':username}))