from django.contrib import admin

# Register your models here.
from .models import Artist, ArtistAlbum, Song, PlatformMix, UserPlaylist, UserPlaylistSong


class ArtistAlbumInline(admin.TabularInline):
    model = ArtistAlbum
    extra = 0


class SongInline(admin.TabularInline):
    model = Song
    extra = 0


class ArtistAdmin(admin.ModelAdmin):
    inlines = [ArtistAlbumInline, SongInline]


class ArtistAlbumAdmin(admin.ModelAdmin):
    inlines = [SongInline]


class UserPlaylistSongInline(admin.TabularInline):
    model = UserPlaylistSong
    extra = 0
    fields = ['song']


class UserPlaylistAdmin(admin.ModelAdmin):
    inlines = [UserPlaylistSongInline]
    list_display = ['name', 'owner']


admin.site.register(Artist, ArtistAdmin)
admin.site.register(ArtistAlbum, ArtistAlbumAdmin)
admin.site.register(Song)
admin.site.register(PlatformMix)
admin.site.register(UserPlaylist, UserPlaylistAdmin)
