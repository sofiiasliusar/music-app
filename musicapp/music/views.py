from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView, DetailView, CreateView, View
from .models import Song, Artist, ArtistAlbum, PlatformMix, UserPlaylist
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import SignUpForm
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404
from .models import UserPlaylist, UserPlaylistSong, Song
import requests


class HomeView(TemplateView):
    template_name = 'Home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # official spotify API
        # top_ukrainian_artists = ["6wbEgVlGqWb4I9tbMluu5Q",  # spotify ids
        #                          "5RqIkHQnXRZlm1ozfSS1IO",
        #                          "5BwbVAdT6rFF2vGVE8su2y",
        #                          "6NTzEgUmN1PIBIYEHhf1kS",
        #                          "2c3PFZtun8HemDbDfRPV6G",
        #                          "7wl1m5vgWkCP3cqYVj2noM",
        #                          "6l5IEx62Nsc2k1QyfaWvEz",
        #                          ]
        #
        # names = []
        # for artist_id in top_ukrainian_artists:
        #     url = "https://spotify-scraper3.p.rapidapi.com/api/artists/info"
        #     params = {"id": artist_id}
        #     headers = {
        #         "x-rapidapi-key": "aa08440083msh782bdf9788498e6p1cd73ejsn7a80b9806eeb",
        #         "x-rapidapi-host": "spotify-scraper3.p.rapidapi.com"
        #     }
        #
        #     response = requests.get(url, headers=headers, params=params)
        #     if response.status_code == 200:
        #         data = response.json()["data"]["artist"]
        #         name = data["name"]
        #         avatar_img = data["avatar_images"][0]["url"]
        #         header_img = data["header_images"][0]["url"]
        #         names.append(name)
        #         artist, created = Artist.objects.get_or_create(
        #             name=name,
        #             defaults={
        #                 "profile_image": avatar_img,
        #                 "detail_image": header_img,
        #             }
        #         )
        #
        #         if created:
        #             print("Artist was just added to the database!")
        #         else:
        #             print("Artist already existed, maybe update info if needed.")
        #
        #         print("Info:"
        #               "\nname- " + name +
        #               "\navatar_img- " + avatar_img +
        #               "\nheader_img- " + header_img)
        #
        # print(names)

        # For now predefines artists
        # todo: Later add feature for user upon sign up to search for artists he wants to listen to
        names = ['MONATIK', 'Скрябін', 'Klavdia Petrivna', 'Okean Elzy', 'Boombox', 'DOROFEEVA', 'Wellboy']

        # context["form"] = CustomUserCreationForm()
        context['new_releases'] = Song.objects.order_by('-release_date')[:6]  # Fetch latest 6 songs
        context['trending_songs'] = Song.objects.order_by('-release_date')[:10]  # Example logic for trending
        context['popular_artists'] = Artist.objects.filter(name__in=names)  # Fetch first 7 artists
        return context


# class RegisterView(CreateView):
#     form_class = CustomUserCreationForm
#     success_url = reverse_lazy("home")  # or any page you want to redirect to
#     template_name = "Home.html"  # not used since we're embedding form
#
#     def form_valid(self, form):
#         response = super().form_valid(form)
#         login(self.request, self.object)  # auto-login after signup
#         return response


class ArtistsView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    template_name = 'Artists.html'


class ArtistDetailView(LoginRequiredMixin, DetailView):
    login_url = 'login'
    model = Artist
    template_name = 'ArtistDetail.html'
    context_object_name = 'artist'
    slug_field = 'slug'  # use slug for lookup
    slug_url_kwarg = 'slug'  # match url parameter

    def get_context_data(self, **kwargs):
        """Add the artist's songs to the context."""
        context = super().get_context_data(**kwargs)
        context['songs'] = self.object.songs.all()
        context['albums'] = self.object.albums.all()
        context['platform_mixes'] = self.object.get_platform_mixes()  # artist playlists
        return context


class AlbumView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    template_name = 'Albums.html'


class PlaylistView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    template_name = 'Playlist.html'

    # def dispatch(self, request, *args, **kwargs):
    #     # Check if the user has a 'MyFavorites' playlist, if not, create it
    #     playlist, created = UserPlaylist.objects.get_or_create(
    #         owner=self.request.user,
    #         name="MyFavorites"
    #     )
    #     # Proceed with the regular dispatch
    #     return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the 'MyFavorites' playlist and its songs
        user = self.request.user
        favorites_playlist = user.userplaylist_set.filter(name="My favorites").first()
        playlist = UserPlaylist.objects.get(owner=self.request.user, name="My favorites")
        context['playlist_songs'] = favorites_playlist.get_songs()  # Get songs in the 'MyFavorites' playlist
        return context


class PremiumView(TemplateView):
    template_name = 'Premium.html'


class SettingsView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    template_name = 'Settings.html'


class AboutView(TemplateView):
    template_name = 'AboutUs.html'


class OfficeView(TemplateView):
    template_name = 'Office.html'


class SongView(LoginRequiredMixin, DetailView):
    login_url = 'login'
    model = Song
    template_name = 'Song.html'
    context_object_name = 'song'
    pk_url_kwarg = 'id'  # Tell Django to use "id" instead of "pk"


class AlbumDetailView(DetailView):
    model = ArtistAlbum
    template_name = "AlbumDetail.html"
    context_object_name = 'album'
    pk_url_kwarg = 'id'


class MixDetailView(DetailView):
    model = PlatformMix
    template_name = "MixDetail.html"
    context_object_name = 'mix'
    pk_url_kwarg = 'id'


class SignUpView(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password1']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                # log the user in
                user_login = authenticate(request, username=username, password=password)
                login(request, user_login)
                next_url = request.POST.get('next') or '/'
                return redirect(next_url)
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            next_url = request.POST.get('next') or '/'
            return redirect(next_url)
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('login')


class SearchView(TemplateView):
    template_name = 'Search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        search_query = self.request.GET.get('search_query', '')

        if search_query:
            # Search Songs
            songs = Song.objects.filter(name__icontains=search_query)
            # Search Artists
            artists = Artist.objects.filter(name__icontains=search_query)
            # Search Albums
            albums = ArtistAlbum.objects.filter(name__icontains=search_query)
        else:
            songs = []
            artists = []
            albums = []

        context['search_query'] = search_query
        context['songs'] = songs
        context['artists'] = artists
        context['albums'] = albums
        favorites = UserPlaylist.objects.filter(owner=self.request.user, name="My favorites").first()
        if favorites:
            context['favorite_song_ids'] = set(favorites.get_songs().values_list('id', flat=True))
        else:
            context['favorite_song_ids'] = set()
        return context


# @method_decorator(csrf_exempt, name='dispatch')  # For simplicity — CSRF token is safer!
# class AddToFavoritesView(LoginRequiredMixin, View):
#     def post(self, request, *args, **kwargs):
#         data = json.loads(request.body)
#         song_id = data.get('song_id')
#         try:
#             song = Song.objects.get(id=song_id)
#             playlist, _ = UserPlaylist.objects.get_or_create(owner=request.user, name="MyFavorites")
#             playlist.songs.add(song)
#             return JsonResponse({'success': True})
#         except Song.DoesNotExist:
#             return JsonResponse({'success': False, 'error': 'Song not found'})

class AddToFavoritesView(View):
    """Class-based view to add a song to the user's 'My favorites' playlist."""

    def post(self, request, song_id):
        user = request.user
        song = get_object_or_404(Song, id=song_id)

        # Get or create the "My favorites" playlist for the user
        favorites_playlist, created = UserPlaylist.objects.get_or_create(owner=user, name="My favorites")

        # Check if the song is already in the playlist
        if not UserPlaylistSong.objects.filter(playlist=favorites_playlist, song=song).exists():
            # Add the song to the playlist
            UserPlaylistSong.objects.create(playlist=favorites_playlist, song=song)
            return JsonResponse({'status': 'added', 'icon': '♥'})
        else:
            return JsonResponse({'status': 'already_added', 'icon': '❤️'})
