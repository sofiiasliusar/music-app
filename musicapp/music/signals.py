from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserPlaylist


@receiver(post_save, sender=User)
def create_favorites_playlist(sender, instance, created, **kwargs):
    """Automatically create an empty 'My favorites' playlist for each new user."""
    if created:
        UserPlaylist.objects.create(owner=instance, name="My favorites")
