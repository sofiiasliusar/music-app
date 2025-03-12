from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Artist(models.Model):
    name = models.CharField(max_length=100)
    genres = models.ManyToManyField(Genre, related_name="artists", blank=True)
    image_url = models.URLField(blank=True, null=True)


    def __str__(self):
        return self.name


class SongCollection(models.Model):
    name = models.CharField(max_length=100)
    image_url = models.URLField(blank=True, null=True)

    def get_total_duration(self):
        return sum(song.duration.total_seconds() for song in self.get_songs())

    def get_amount_of_songs(self):
        return self.get_songs().count()

    def get_songs(self):
        raise NotImplementedError("Subclasses must implement the get_songs method.")

    def __str__(self):
        return self.name


class ArtistAlbum(SongCollection):
    owner = models.ForeignKey('Artist', on_delete=models.CASCADE)
    release_date = models.DateField()
    genres = models.ManyToManyField(Genre, related_name="albums", blank=True)

    def get_songs(self):
        return self.songs.all()


class Song(models.Model):
    name = models.CharField(max_length=100)
    artist = models.ForeignKey(Artist,  related_name='songs', on_delete=models.CASCADE)
    album = models.ForeignKey(ArtistAlbum, related_name='songs',  on_delete=models.CASCADE, null=True, blank=True)
    duration = models.DurationField()
    release_date = models.DateField()
    audio_url = models.URLField()
    lyrics = models.TextField(blank=True, null=False)
    genres = models.ManyToManyField(Genre, related_name="songs", blank=True)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} by {self.artist.name}"


class PlatformMix(SongCollection):
    owner = models.CharField(max_length=255, default="Melonix")
    songs = models.ManyToManyField(Song, related_name='mixes')
    genres = models.ManyToManyField(Genre, related_name="mixes", blank=True)

    def get_songs(self):
        return self.songs.all()


class UserPlaylist(SongCollection):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_songs(self):
        return Song.objects.filter(userplaylistsong__playlist=self)

    # def update_image_from_first_song(self):
    #     """Automatically set the playlist image to the first song's image_url."""
    #     first_song = self.get_songs().first()
    #     if first_song and first_song.image_url:
    #         self.image_url = first_song.image_url
    #         self.save()


class UserPlaylistSong(models.Model):
    playlist = models.ForeignKey(UserPlaylist, on_delete=models.CASCADE)
    # when playlist is deleted, all UserPlaylistSongs will be deleted too
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    # when Song is deleted, in all playlists this song will be deleted
    date_added = models.DateField(auto_now_add=True)

    class Meta:  # ensures that the same song cannot be added to the same playlist twice
        constraints = [
            models.UniqueConstraint(fields=['playlist', 'song'], name='unique_playlist_song')
        ]
