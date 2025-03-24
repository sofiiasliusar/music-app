from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView, DetailView
from .models import Song, Artist


class HomeView(TemplateView):
    template_name = 'Home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['new_releases'] = Song.objects.order_by('-release_date')[:6]  # Fetch latest 6 songs
        context['trending_songs'] = Song.objects.order_by('-release_date')[:7]  # Example logic for trending
        context['popular_artists'] = Artist.objects.all()[:7]  # Fetch first 6 artists
        return context


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
        return context


class AlbumView(TemplateView):
    template_name = 'Albums.html'


class PlaylistView(TemplateView):
    template_name = 'Playlist.html'


class PremiumView(TemplateView):
    template_name = 'Premium.html'


class SettingsView(TemplateView):
    template_name = 'Settings.html'


class AboutView(TemplateView):
    template_name = 'AboutUs.html'


class OfficeView(TemplateView):
    template_name = 'Office.html'
