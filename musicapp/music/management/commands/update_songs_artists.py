from django.core.management import BaseCommand

from ...models import Song, Artist
import requests
import datetime

class Command(BaseCommand):
    help = 'Update all songs with their corresponding artists'

    def handle(self, *args, **kwargs):
        # Fetch all songs
        songs = Song.objects.all()

        for song in songs:
            if song.artists.exists():
                print(f"Song {song.name} already has artists. Skipping.")
                continue

            print(f"Updating song: {song.name}")

            track_id = song.spotify_id

            # Fetch track details from Spotify API
            token = "BQApmZ2OcrLSKF9bzECazj5l79Wk2wvhEPfubIVwA6sTIiFcTb7EZRG7YCNFjpGTImZLEYdym6bJ_s-LuB8QLb8LAVBsM8WYGd0mIUxC7nntMYvFZ1Yk6ywC30LK0O9nk7qdHmQi8lQ"
            headers = {
                'Authorization': f'Bearer {token}',
            }
            track_url = f'https://api.spotify.com/v1/tracks/{track_id}'
            params = {'market': 'UA'}

            response = requests.get(track_url, headers=headers, params=params)

            if response.status_code != 200:
                print(f"Failed to fetch track info for {song.name}")
                continue

            track_data = response.json()
            artists_data = track_data.get('artists', [])

            artist_objs = []
            for artist_info in artists_data:
                artist_id = artist_info["id"]
                artist_name = artist_info["name"]

                # Check if artist exists
                artist = Artist.objects.filter(spotify_id=artist_id).first()
                if not artist:
                    # Fetch artist details from your scraper API
                    artist_url = "https://spotify-scraper3.p.rapidapi.com/api/artists/info"
                    params = {"id": artist_id}
                    headers_scraper = {
                        "x-rapidapi-key": "YOUR_RAPID_API_KEY",
                        "x-rapidapi-host": "spotify-scraper3.p.rapidapi.com"
                    }

                    artist_response = requests.get(artist_url, headers=headers_scraper, params=params)
                    if artist_response.status_code == 200:
                        data = artist_response.json().get("data", {}).get("artist", {})
                        if data:
                            avatar_img = data["avatar_images"][0]["url"] if data.get("avatar_images") else None
                            header_img = data["header_images"][0]["url"] if data.get("header_images") else None

                            artist = Artist.objects.create(
                                spotify_id=artist_id,
                                name=artist_name,
                                profile_image=avatar_img,
                                detail_image=header_img,
                            )
                            print(f"Created artist: {artist_name}")
                        else:
                            print(f"No artist data found for {artist_name}")
                            continue
                    else:
                        print(f"Failed to fetch artist info for {artist_name}")
                        continue

                artist_objs.append(artist)

            # Set artists for song
            if artist_objs:
                song.artists.set(artist_objs)
                print(f"Updated song {song.name} with {len(artist_objs)} artist(s).")
            else:
                print(f"No artists found for {song.name}")

        print("Finished updating songs.")
