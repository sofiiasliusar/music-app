from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'Home.html'


class ArtistsView(TemplateView):
    template_name = 'Artists.html'


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
