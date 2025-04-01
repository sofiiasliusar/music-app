from . import views
from django.urls import path

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name="about"),
    path('artists/', views.ArtistsView.as_view(), name="artists"),
    path('albums/', views.AlbumView.as_view(), name="albums"),
    path('playlist/', views.PlaylistView.as_view(), name="playlist"),
    path('premium/', views.PremiumView.as_view(), name="premium"),
    path('settings/', views.SettingsView.as_view(), name="settings"),
    path('office/', views.OfficeView.as_view(), name="office"),
    path('artist/<slug:slug>/', views.ArtistDetailView.as_view(), name='artist_detail'),
    path('song/<int:id>/', views.SongView.as_view(), name='song'),
]
