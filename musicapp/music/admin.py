import datetime
from django.contrib import admin
from .utils import image_preview_detail, image_preview_list

# Register your models here.
from .models import Artist, ArtistAlbum, Song, PlatformMix, UserPlaylist, UserPlaylistSong, Genre


class SongCollectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'image_preview_list', 'get_total_duration', 'get_amount_of_songs']
    readonly_fields = ('image_preview_detail',)

    def get_total_duration(self, obj):
        return obj.get_total_duration()

    def get_amount_of_songs(self, obj):
        return obj.get_amount_of_songs()

    image_preview_detail = staticmethod(image_preview_detail)
    image_preview_list = staticmethod(image_preview_list)
    get_total_duration.short_description = "Total Duration"
    get_amount_of_songs.short_description = "Number of Songs"


class SongAdmin(admin.ModelAdmin):
    list_display = ['name', 'image_preview_list', 'release_date', 'album', 'duration']
    readonly_fields = ('image_preview_detail',)
    image_preview_detail = staticmethod(image_preview_detail)
    image_preview_list = staticmethod(image_preview_list)


class ArtistAlbumInline(admin.TabularInline):
    model = ArtistAlbum
    extra = 0


# class SongInline(admin.TabularInline):
#     model = Song
#     extra = 0


class ArtistAdmin(admin.ModelAdmin):
    inlines = [ArtistAlbumInline]

    def change_view(self, request, object_id, form_url='', extra_context=None):
        artist = self.get_object(request, object_id)
        # Fetch related songs using the ManyToMany relationship
        songs = Song.objects.filter(artists=artist)

        # Add the songs to the context
        if extra_context is None:
            extra_context = {}
        extra_context['songs'] = songs

        return super().change_view(request, object_id, form_url, extra_context=extra_context)


class ArtistAlbumAdmin(SongCollectionAdmin):
    list_display = SongCollectionAdmin.list_display + ['owner', 'release_date', "get_songs"]  # Add extra fields

    def get_songs(self, obj):
        return ", ".join(song.name for song in obj.songs.all())

    get_songs.short_description = 'Songs'

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
admin.site.register(Song, SongAdmin)
admin.site.register(PlatformMix, PlatformMixAdmin)
admin.site.register(UserPlaylist, UserPlaylistAdmin)
admin.site.register(Genre)

