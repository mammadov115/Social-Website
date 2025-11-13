from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Image

@receiver(m2m_changed, sender=Image.users_like.through)
def users_like_changed(sender, instance, **kwargs):
    """
    Signal handler to update the total_likes field whenever the users_like
    ManyToManyField changes (user likes/unlikes an image).

    Args:
        sender: The model class sending the signal (through table of users_like).
        instance: The Image instance being modified.
        **kwargs: Additional keyword arguments from the signal.
    """
    # Count the current number of users who liked this image
    instance.total_likes = instance.users_like.count()
    # Save the updated total_likes value
    instance.save()
