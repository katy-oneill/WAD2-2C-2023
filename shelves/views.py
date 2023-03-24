from django.shortcuts import render, redirect
from django.http import HttpResponse
from shelves.form import RegistrationForm, MediaForm, BookForm, MovieForm, ShowForm, SongForm, PostForm
from django.contrib.auth import login, logout
from shelves.models import Media, Book, Movie, Show, Song, Post, UserProfile
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse

def launch(request):
    if request.user.is_authenticated:
        return render(request, 'shelves/dashboard.html')
    else:
        return render(request, 'shelves/launch.html')

def friends(request):
    return render(request, 'shelves/friends.html')

def profile(request):
    return render(request, 'shelves/profile.html')

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

            if media.type == "book":
                return redirect(reverse('shelves:add_book_details', kwargs={'media_title_slug': media.slug}))
            elif media.type == "movie":
                return redirect(reverse('shelves:add_movie_details', kwargs={'media_title_slug': media.slug}))
            elif media.type == "show":
                return redirect(reverse('shelves:add_show_details', kwargs={'media_title_slug': media.slug}))
            elif media.type == "song":
                return redirect(reverse('shelves:add_song_details', kwargs={'media_title_slug': media.slug}))

        else:
            print(media_form.errors)

    return render(request, 'shelves/add_media.html', {'form': media_form})


@login_required
def add_book_details(request, media_title_slug):
    try:
        media = Media.objects.get(slug=media_title_slug)
    except Media.DoesNotExist:
        media = None

    if media is None:
        return redirect(reverse('shelves:add_media'))

    book_form = BookForm()

    if request.method == 'POST':
        book_form = BookForm(request.POST)

        if book_form.is_valid():
            book = book_form.save(commit=False)
            book.media = media
            book.save()

            return redirect(reverse('shelves:show_media',
                                    kwargs={'media_title_slug':
                                            media_title_slug,
                                            'media_type':
                                            book.media.type}))
        else:
            print(book_form.errors)

    context_dict = {'form': book_form, 'media': media}
    return render(request, 'shelves/add_book_details.html', context=context_dict)


@login_required
def add_movie_details(request, media_title_slug):
    try:
        media = Media.objects.get(slug=media_title_slug)
    except Media.DoesNotExist:
        media = None

    if media is None:
        return redirect(reverse('shelves:add_media'))

    movie_form = MovieForm()

    if request.method == 'POST':
        movie_form = MovieForm(request.POST)

        if movie_form.is_valid():
            movie = movie_form.save(commit=False)
            movie.media = media
            movie.save()

            return redirect(reverse('shelves:show_media',
                            kwargs={'media_title_slug':
                                    media_title_slug,
                                    'media_type':
                                    movie.media.type}))
        else:
            print(movie_form.errors)

    context_dict = {'form': movie_form, 'media': media}
    return render(request, 'shelves/add_movie_details.html', context=context_dict)


@login_required
def add_show_details(request, media_title_slug):
    try:
        media = Media.objects.get(slug=media_title_slug)
    except Media.DoesNotExist:
        media = None

    if media is None:
        return redirect(reverse('shelves:add_media'))

    show_form = ShowForm()

    if request.method == 'POST':
        show_form = ShowForm(request.POST)

        if show_form.is_valid():
            show = show_form.save(commit=False)
            show.media = media
            show.save()

            return redirect(reverse('shelves:show_media',
                            kwargs={'media_title_slug':
                                    media_title_slug,
                                    'media_type':
                                    show.media.type}))
        else:
            print(show_form.errors)

    context_dict = {'form': show_form, 'media': media}
    return render(request, 'shelves/add_show_details.html', context=context_dict)


@login_required
def add_song_details(request, media_title_slug):
    try:
        media = Media.objects.get(slug=media_title_slug)
    except Media.DoesNotExist:
        media = None

    if media is None:
        return redirect(reverse('shelves:add_media'))

    song_form = SongForm()

    if request.method == 'POST':
        song_form = SongForm(request.POST)

        if song_form.is_valid():
            song = song_form.save(commit=False)
            song.media = media
            song.save()

            return redirect(reverse('shelves:show_media',
                            kwargs={'media_title_slug':
                                    media_title_slug,
                                    'media_type':
                                    song.media.type}))
        else:
            print(song_form.errors)

    context_dict = {'form': song_form, 'media': media}
    return render(request, 'shelves/add_song_details.html', context=context_dict)


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

                return redirect(reverse('shelves:show_media',
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

