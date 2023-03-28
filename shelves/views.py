from django.shortcuts import render, redirect
from shelves.models import Media, Book, Movie, Show, Song, Post, UserProfile, FriendRequest
from shelves.forms import MediaForm, BookForm, MovieForm, ShowForm, SongForm, PostForm, UserProfileForm, ProfileUpdateForm, RegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.urls import reverse
from django.contrib.auth.models import User
from django.views import View
from django.utils.decorators import method_decorator

#--------------------------------------------------------------------------
def index(request):
    context_dict = {}

    try:
        media_list = Media.objects.order_by('-avgScore')[:10]
        post_list = Post.objects.order_by('-likes')[:10]

        context_dict['medias'] = media_list
        context_dict['posts'] = post_list
    
    except Media.DoesNotExist:
        context_dict['medias'] = None
        context_dict['posts'] = None

    response = render(request, 'shelves/index.html', context=context_dict)

    return response


def show_media(request, media_title_slug, media_type):
    context_dict = {}
    
    try:
        
        media = Media.objects.get(slug=media_title_slug, type=media_type)
        try:
            if request.user:
                user = UserProfile.objects.get_or_create(user=request.user)[0]
                user_friends = user.friends.all()
                posts = []
                if user_friends:
                    for friend in user_friends:
                        posts = posts + list(Post.objects.filter(media=media, user=friend.user))
                
                # Since user and media are linked uniquely in Post model
                posts = posts + list(Post.objects.filter(media=media, user=user.user))
        except:
            posts = None
        
        context_dict['media'] = media
        context_dict['posts'] = posts
    
    except Media.DoesNotExist:
        context_dict['media'] = None
        context_dict['posts'] = None

    return render(request, 'shelves/media.html', context=context_dict)


def list_media(request):
    media_collection = {}

    book_list = Book.objects.all()
    movie_list = Movie.objects.all()
    show_list = Show.objects.all()
    song_list = Song.objects.all()

    media_collection['books'] = book_list
    media_collection['movies'] = movie_list
    media_collection['shows'] = show_list
    media_collection['songs'] = song_list

    context_dict = {}
    context_dict['media_collection'] = media_collection
    
    response = render(request, 'shelves/list_media.html', context=context_dict)

    return response


@login_required
def add_media(request):
    media_form = MediaForm()

    if request.method == 'POST':
        media_form = MediaForm(request.POST)

        if media_form.is_valid():
            media = media_form.save(commit=False)
            media.user = request.user
            media.save()
            return redirect(reverse('shelves:add_details', kwargs={'media_title_slug': media.slug,
                                                                   'media_type': media.type}))
        else:
            print(media_form.errors)

    return render(request, 'shelves/add_media.html', {'form': media_form})


@login_required
def add_details(request, media_title_slug, media_type):
    try:
        media = Media.objects.get(slug=media_title_slug, type=media_type)
    except Media.DoesNotExist:
        media = None

    if media is None:
        return redirect(reverse('shelves:add_media'))
    
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

            return redirect(reverse('shelves:show_media',
                                    kwargs={'media_title_slug':
                                            media_title_slug,
                                            'media_type':
                                            media.type}))
        else:
            print(type_form.errors)

    context_dict = {'form': type_form, 'media': media}
    return render(request, 'shelves/add_details.html', context=context_dict)


@login_required
def add_post(request, media_title_slug, media_type):
    try:
        media = Media.objects.get(slug=media_title_slug, type=media_type)
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
                                                media_title_slug,
                                                'media_type':
                                                media.type}))
        else:
            print(post_form.errors)

    context_dict = {'form': post_form, 'media': media}
    return render(request, 'shelves/add_post.html', context=context_dict)


class ProfileView(View):
    def get_user_details(self, username, request):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        
        user_profile = UserProfile.objects.get_or_create(user=user)[0]
        form = UserProfileForm({'picture': user_profile.picture,})
        user_posts = Post.objects.filter(user = user.id)
        user_collection = Media.objects.filter(user = user.id)

        media_dict = {}
        media_dict['books'] = user_collection.filter(type='book')
        media_dict['movies'] = user_collection.filter(type='movie')
        media_dict['shows'] = user_collection.filter(type='show')
        media_dict['songs'] = user_collection.filter(type='song')

        friend_dict = {}
        if request.user == user:
            incoming_friend_requests = FriendRequest.objects.filter(receiver=user_profile.user)
            friend_dict['incoming_friend_requests'] = [request.sender for request in list(incoming_friend_requests)]
        
        else:
            friend_dict['selected_user_friends'] = user_profile.friends.all()
            friend_dict['self'] = UserProfile.objects.get(user=request.user)
            try:
                friend_dict['inbound_friend_request'] = FriendRequest.objects.get(receiver=request.user, sender=user_profile.user)
            except:
                friend_dict['inbound_friend_request'] = None
            try:
                friend_dict['outbound_friend_request'] = FriendRequest.objects.get(receiver=user_profile.user, sender=request.user)
            except:
                friend_dict['outbound_friend_request'] = None
        
        return (user, user_profile, form, user_posts, media_dict, friend_dict)
    
    @method_decorator(login_required)
    def get(self, request, username):
        try:
            (user, user_profile, form, posts, media_collection, friend_dict) = self.get_user_details(username, request)
        except TypeError:
            return redirect(reverse('shelves:index'))
        
        context_dict = {'user_profile': user_profile,
                        'selected_user': user,
                        'form': form,
                        'posts': posts,
                        'media_collection': media_collection,
                        }
        
        context_dict.update(friend_dict)
        return render(request, 'shelves/profile.html', context_dict)
    
    @method_decorator(login_required)
    def post(self, request, username):
        try:
            (user, user_profile, form,  posts, media_collection, friend_dict) = self.get_user_details(username, request)
        except TypeError:
            return redirect(reverse('shelves:index'))

        form = UserProfileForm(
            request.POST, request.FILES, instance=user_profile)

        if form.is_valid():
            form.save(commit=True)
            return redirect('shelves:profile', user.username)
        else:
            print(form.errors)

        context_dict = {'user_profile': user_profile,
                        'selected_user': user,
                        'form': form,
                        'posts': posts,
                        'media_collection': media_collection,
                        }
        
        context_dict.update(friend_dict)
        return render(request, 'shelves/profile.html', context_dict)


@login_required
def delete_account(request, username):
    user = User.objects.get(username=username)
    if request.method == 'POST':
        user.delete()
        return redirect('/')

    return render(request, 'profile.html', {'user': user})


class ListProfilesView(View):
    @method_decorator(login_required)
    def get(self, request):
        profiles = UserProfile.objects.all()
        return render(request,
                    'shelves/list_profiles.html',
                    {'user_profile_list': profiles})


def about(request):
    context_dict = {}

    return render(request, 'shelves/about.html', context=context_dict)


def contact(request):
    context_dict = {}

    return render(request, 'shelves/contact.html', context=context_dict)


@login_required
def send_friend_request(request, username):
    sender = request.user
    receiver = User.objects.get(username=username)
    
    FriendRequest.objects.get_or_create(sender=sender, receiver=receiver)
    return redirect(reverse('shelves:profile', kwargs={'username':username}))


@login_required
def accept_friend_request(request, username):
    receiver = request.user
    sender = User.objects.get(username=username)

    try:
        friend_request = FriendRequest.objects.get(sender=sender, receiver=receiver)
    except:
        friend_request = None

    if friend_request != None:
        receiver = UserProfile.objects.get(user=receiver)
        sender = UserProfile.objects.get(user=sender)
        
        sender.friends.add(receiver)
        receiver.friends.add(sender)
        friend_request.delete()
    
    return redirect(reverse('shelves:profile', kwargs={'username':username}))
#--------------------------------------------------------------------------


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
    return redirect('shelves:launch')

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
    context = {'user': user, 'shelves:profile': profile}
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

    context = {'user': user, 'shelves:profile_form': profile_form}
    return render(request, 'shelves/edit_profile.html', context)

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
            return redirect('shelves:registration_success')
    else:
        form = RegistrationForm()
    return render(request, 'shelves/register.html', {'form': form})

def registration_success(request):
    user_profile = request.user.userprofile
    return redirect(reverse('shelves:dashboard'))

# @login_required
def dashboard(request):
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = None
    return render(request, 'shelves/dashboard.html', {'user_profile': user_profile})
