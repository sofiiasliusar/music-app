import datetime
from django.contrib import admin

# Register your models here.
from .models import Artist, ArtistAlbum, Song, PlatformMix, UserPlaylist, UserPlaylistSong, Genre


class SongCollectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_total_duration', 'get_amount_of_songs']

    def get_total_duration(self, obj):
        total_seconds = obj.get_total_duration()
        return str(datetime.timedelta(seconds=int(total_seconds)))  # Formats as HH:MM:SS

    def get_amount_of_songs(self, obj):
        return obj.get_amount_of_songs()

    get_total_duration.short_description = "Total Duration"
    get_amount_of_songs.short_description = "Number of Songs"


class ArtistAlbumInline(admin.TabularInline):
    model = ArtistAlbum
    extra = 0


class SongInline(admin.TabularInline):
    model = Song
    extra = 0


class ArtistAdmin(admin.ModelAdmin):
    inlines = [ArtistAlbumInline, SongInline]


class ArtistAlbumAdmin(SongCollectionAdmin):
    inlines = [SongInline]
    list_display = SongCollectionAdmin.list_display + ['owner', 'release_date']  # Add extra fields


class UserPlaylistSongInline(admin.TabularInline):
    model = UserPlaylistSong
    extra = 0
    fields = ['song']


class UserPlaylistAdmin(SongCollectionAdmin):
    inlines = [UserPlaylistSongInline]
    list_display = SongCollectionAdmin.list_display + ['owner']


class PlatformMixAdmin(SongCollectionAdmin):
    list_display = SongCollectionAdmin.list_display + ['owner']


admin.site.register(Artist, ArtistAdmin)
admin.site.register(ArtistAlbum, ArtistAlbumAdmin)
admin.site.register(Song)
admin.site.register(PlatformMix, PlatformMixAdmin)
admin.site.register(UserPlaylist, UserPlaylistAdmin)
admin.site.register(Genre)

