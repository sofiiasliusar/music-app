from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView, DetailView, CreateView
from .models import Song, Artist, ArtistAlbum, PlatformMix
# from django.urls import reverse_lazy
# from django.contrib.auth import login
# from .forms import CustomUserCreationForm


class HomeView(TemplateView):
    template_name = 'Home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["form"] = CustomUserCreationForm()
        context['new_releases'] = Song.objects.order_by('-release_date')[:6]  # Fetch latest 6 songs
        context['trending_songs'] = Song.objects.order_by('-release_date')[:10]  # Example logic for trending
        context['popular_artists'] = Artist.objects.all()[:7]  # Fetch first 7 artists
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

class ArtistsView(TemplateView):
    template_name = 'Artists.html'


class ArtistDetailView(DetailView):
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


class AlbumView(TemplateView):
    template_name = 'Albums.html'


class PlaylistView(TemplateView):
    template_name = 'Playlist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['playlist_songs'] = Song.objects.order_by('-release_date')[:5]  # Example logic for playlist
        return context

class PremiumView(TemplateView):
    template_name = 'Premium.html'


class SettingsView(TemplateView):
    template_name = 'Settings.html'


class AboutView(TemplateView):
    template_name = 'AboutUs.html'


class OfficeView(TemplateView):
    template_name = 'Office.html'


class SongView(DetailView):
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


class SignupView(TemplateView):
    template_name = 'Signup.html'


class LoginView(TemplateView):
    template_name = 'Login.html'
