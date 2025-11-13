from django.contrib.auth.models import User
from account.models import Profile

# -------------------------------
# Custom Authentication Backend
# -------------------------------
class EmailAuthBackend:
    """
    Authenticate users using their email address instead of username.

    Methods:
        authenticate(request, username, password): Returns User if credentials are valid.
        get_user(user_id): Returns User instance for given ID or None if not found.
    """

    def authenticate(self, request, username=None, password=None):
        """
        Authenticate a user based on email and password.

        Args:
            request (HttpRequest): The HTTP request object.
            username (str): Email address of the user.
            password (str): User's password.

        Returns:
            User instance if authentication is successful, otherwise None.
        """
        try:
            # Look up user by email
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None

    def get_user(self, user_id):
        """
        Retrieve a User instance by primary key.

        Args:
            user_id (int): Primary key of the user.

        Returns:
            User instance if found, else None.
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

# -------------------------------
# Pipeline function for social auth
# -------------------------------
def create_profile(backend, user, *args, **kwargs):
    """
    Create a Profile for newly registered users if it doesn't exist.

    This is useful for social authentication pipelines where a User may
    be created automatically, and a corresponding Profile must also exist.

    Args:
        backend: The authentication backend used (ignored here).
        user (User): The newly created User instance.
    """
    Profile.objects.get_or_create(user=user)
