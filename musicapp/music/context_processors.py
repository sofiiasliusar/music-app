from .models import UserPlaylist


def favorite_song_ids(request):
    if not request.user.is_authenticated:
        return {'favorite_song_ids': set()}

    favorites = UserPlaylist.objects.filter(owner=request.user, name="My favorites").first()
    if favorites:
        favorite_ids = set(favorites.get_songs().values_list('id', flat=True))
    else:
        favorite_ids = set()

    return {'favorite_song_ids': favorite_ids}
