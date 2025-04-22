from django.db.models import Q
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
from googletrans import Translator
import base64
from dotenv import load_dotenv
import os
import datetime
from langdetect import detect
from bs4 import BeautifulSoup
import time
import random

load_dotenv()


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
        # top_ukrainian_artists = ["11sIz9STeD6yVSuBaD8nMW"]
        #
        # names = []
        #
        # # SCRAPER FOR IMAGES (INCLUDING HEADER IMAGE)
        # for artist_id in top_ukrainian_artists:
        #     print("HELLOOO")
        #     url = "https://spotify-scraper3.p.rapidapi.com/api/artists/info"
        #     params = {"id": artist_id}
        #     headers = {
        #         "x-rapidapi-key": "aa08440083msh782bdf9788498e6p1cd73ejsn7a80b9806eeb",
        #         "x-rapidapi-host": "spotify-scraper3.p.rapidapi.com"
        #     }
        #
        #     response = requests.get(url, headers=headers, params=params)
        #     print(response)
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
        #                 "spotify_id": artist_id,
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
        context['new_releases'] = Song.objects.filter(
            artists__name__in=names
        ).exclude(
            Q(audio_url="https://example.com") | Q(lyrics="")
        ).order_by('-release_date')[:6]
        # context['new_releases'] = Song.objects.order_by('-release_date')[:6]  # Fetch latest 6 songs
        context['trending_songs'] = Song.objects.filter(
        artists__name__in=names
        ).exclude(
            Q(audio_url="https://example.com") | Q(lyrics="")
        ).order_by('-popularity')[:10]
        # context['trending_songs'] = Song.objects.order_by('-release_date')[:10]  # Example logic for trending
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
        artist_id = self.object.spotify_id
        print(artist_id)
        artist_name = self.object.name

        def get_spotify_api_token():
            client_id = os.getenv("SPOTIFY_ID")
            client_secret = os.getenv("SPOTIFY_SECRET")
            auth_str = f"{client_id}:{client_secret}"
            b64_auth = base64.b64encode(auth_str.encode()).decode()

            response = requests.post(
                'https://accounts.spotify.com/api/token',
                headers={
                    'Authorization': f'Basic {b64_auth}',
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                data={'grant_type': 'client_credentials'}
            )

            return response.json()['access_token']

        def get_top_10_tracks():
            token = get_spotify_api_token()
            market = 'UA'

            url = f'https://api.spotify.com/v1/artists/{artist_id}/top-tracks'
            headers = {
                'Authorization': f'Bearer {token}',
            }
            params = {
                'market': market
            }

            response = requests.get(url, headers=headers, params=params)
            print(response)
            if response.status_code == 200:
                return response.json()["tracks"]

        def get_lyrics_from_genius(song_title):

            if song_title == "Забий":
                song_title = "Let It Go"
            elif song_title == "ДІВ ЧИНА":
                song_title = "Girl"
            elif song_title == "Вишнi":
                song_title = "Cherries"
            else:
                lang = detect(song_title)
                if lang != "en":
                    translator = Translator()
                    song_title = translator.translate(song_title, src='uk', dest='en').text
            search_for = f"{song_title} {artist_name}"
            print(search_for)

            search_endpoint = "https://api.genius.com/search"
            headers = {
                'Authorization': f'Bearer {os.getenv("GENIUS_TOKEN")}',
            }
            params = {
                'q': search_for
            }

            response = requests.get(search_endpoint, headers=headers, params=params)
            if response.status_code == 200 and response.json()["response"]["hits"]:
                print(artist_name)
                print(response.json()["response"]["hits"][0]["result"]["artist_names"])
                print(artist_name in response.json()["response"]["hits"][0]["result"]["artist_names"])
                if response.json()["response"]["hits"][0]["result"]["lyrics_state"] == "complete"\
                        and artist_name in response.json()["response"]["hits"][0]["result"]["artist_names"]:

                    base = "https://genius.com"
                    endpoint = response.json()["response"]["hits"][0]["result"]["path"]
                    link = base + endpoint
                    print(link)
                    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"}
                    response = requests.get(url=link, headers=header)

                    contents = response.text
                    soup = BeautifulSoup(contents, "html.parser")
                    lyrics_container = soup.find_all(class_="Lyrics__Container-sc-78fb6627-1 hiRbsH")

                    text = "\n".join([block.get_text(separator="\n") for block in lyrics_container]).splitlines()
                    lyrics = "\n".join(text[2:])
                    print(lyrics)

                    return lyrics
                return ""


        def get_song_url_from_soundcloud(name):
            scraper_url = "https://spotify-scraper.p.rapidapi.com/v1/track/download/soundcloud"

            querystring = {"track": f"{name} {artist_name}", "quality": "sq"}

            headers = {
                "x-rapidapi-key": os.getenv("RAPID_API_KEY"),
                "x-rapidapi-host": "spotify-scraper.p.rapidapi.com"
            }

            scraper_data = requests.get(scraper_url, headers=headers, params=querystring).json()
            if "soundcloudTrack" in scraper_data:
                return scraper_data["soundcloudTrack"]["audio"][0]["url"]
            else:
                return "https://example.com"

        def get_track_preview_from_spotify(song_id):
            track_url = f"https://open.spotify.com/track/{song_id}"

            response = requests.get(track_url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                og_audio_tag = soup.find('meta', property='og:audio')

                if og_audio_tag:
                    url = og_audio_tag.get('content')
                    print(url)
                    return url
                else:
                    print("Audio URL not found in the meta tags.")
                    return "https://fakeurl.com"
            else:
                print(f"Error: Unable to fetch the page. Status code: {response.status_code}")
                return "https://fakeurl.com"

        # artist_top_songs = get_top_10_tracks()
        # print(artist_top_songs)
        # for song in artist_top_songs:
        #     song_name = song["name"]
        #     spotify_id = song["id"]
        #     print(f"Adding song - {song_name}")
        #     duration = datetime.timedelta(milliseconds=song["duration_ms"])
        #     release_date = song["album"]["release_date"]
        #     if len(release_date) == 4:
        #         release_date = datetime.datetime.strptime(release_date + "-01-01", "%Y-%m-%d").date()
        #
        #     artist_objs = []
        #
        #     for artist in song["artists"]:
        #         print(artist["name"])
        #         artist_obj, _ = Artist.objects.get_or_create(
        #             spotify_id=artist["id"],
        #             defaults={"name": artist["name"]}
        #         )
        #         artist_objs.append(artist_obj)
        #
        #     lyrics = get_lyrics_from_genius(song_name)
        #     if lyrics:
        #         lang = detect(lyrics)
        #         if lang == "ru":
        #             "song_name is in russian - nonono"
        #             continue
        #     popularity = song["popularity"]
        #     audio_url = get_track_preview_from_spotify(spotify_id)
        #     album = None
        #     image_url = None
        #
        #     album_type = song["album"]["album_type"]
        #     if album_type == "single":
        #         image_url = song["album"]["images"][0]["url"]
        #     elif album_type == "album":
        #         album_id = song["album"]["id"]
        #         album = ArtistAlbum.objects.filter(spotify_id=album_id).first()
        #
        #         if not album:
        #             print("Album not found. Creating...")
        #             release_date = song["album"]["release_date"]
        #             if len(release_date) == 4:
        #                 release_date = datetime.datetime.strptime(release_date + "-01-01", "%Y-%m-%d").date()
        #
        #             album = ArtistAlbum.objects.create(
        #                 name=song["album"]["name"],
        #                 owner=self.object,
        #                 release_date=release_date,
        #                 image_url=song["album"]["images"][0]["url"],
        #                 spotify_id=album_id
        #             )
        #     song, created = Song.objects.get_or_create(
        #         spotify_id=spotify_id,
        #         defaults={
        #             "name": song_name,
        #             "album": album,
        #             "duration": duration,
        #             "release_date": release_date,
        #             "audio_url": audio_url,
        #             "lyrics": lyrics if lyrics else "",
        #             "image_url": image_url if image_url else None,
        #             "popularity": popularity,
        #         }
        #     )
        #
        #     if created:
        #         song.artists.set(artist_objs)  # use .set() to assign all at once
        #     else:
        #         song.artists.add(*artist_objs)

        # UPDATE LYRICS
        #     if not created and lyrics:
        #         # Only update lyrics if the song already exists and lyrics is provided
        #         print("Updating lyrics...")
        #         song.lyrics = lyrics
        #         song.save(update_fields=['lyrics'])

        # UPDATE AUDIO WITH PREVIEW
        # for song in self.object.songs.all():
        #     audio_url = get_track_preview_from_spotify(song.spotify_id)
        #
        #     if audio_url:
        #         song.audio_url = audio_url
        #         song.save(update_fields=['audio_url'])
        #     time.sleep(random.uniform(1, 3))

        context['songs'] = Song.objects.filter(artists=self.object)[:10]
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
