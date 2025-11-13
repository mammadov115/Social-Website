from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

# -------------------------------
# User Profile Model
# -------------------------------
class Profile(models.Model):
    """
    Extends the default user model to store additional info for each user.

    Fields:
        user (OneToOneField): Links Profile to Django's built-in User model.
        date_of_birth (DateField): Optional date of birth of the user.
        photo (ImageField): Optional profile picture, stored in 'users/YYYY/MM/DD/'.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)

    def __str__(self):
        return f'Profile of {self.user.username}'

# -------------------------------
# Contact Model for Following System
# -------------------------------
class Contact(models.Model):
    """
    Represents a "following" relationship between two users.

    Fields:
        user_from (ForeignKey): The user who is following another user.
        user_to (ForeignKey): The user being followed.
        created (DateTimeField): Timestamp when the follow action occurred.
    """
    user_from = models.ForeignKey('auth.User', related_name='rel_from_set', on_delete=models.CASCADE)
    user_to = models.ForeignKey('auth.User', related_name='rel_to_set', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        # For fast querying by creation time
        indexes = [
            models.Index(fields=['-created']),
        ]
        # Default ordering: newest first
        ordering = ['-created']

    def __str__(self):
        # Corrected typo: user_form → user_from
        return f'{self.user_from} follows {self.user_to}'

# -------------------------------
# Extend User Model Dynamically
# -------------------------------
user_model = get_user_model()
user_model.add_to_class(
    'following',
    models.ManyToManyField(
        'self',
        through=Contact,  # Uses Contact model as the intermediate table
        related_name='followers',  # Allows reverse lookup: user.followers
        symmetrical=False  # Following is directional (not mutual by default)
    )
)
