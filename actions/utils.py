from django.contrib.contenttypes.models import ContentType
from .models import Action
from django.utils import timezone
import datetime

def create_action(user, verb, target=None):
    """
    Logs a user action, preventing duplicate actions in a short time window.

    Args:
        user: User instance performing the action.
        verb: Description of the action (e.g., 'liked', 'followed').
        target: Optional model instance that is the target of the action.

    Returns:
        True if a new action was created, False if a similar action already exists.
    """
    now = timezone.now()
    last_minute = now - datetime.timedelta(seconds=60)

    # Filter for recent similar actions by the same user
    similar_actions = Action.objects.filter(
        user_id=user.id,
        verb=verb,
        created__gte=last_minute
    )

    # If a target object is specified, filter by it
    if target:
        target_ct = ContentType.objects.get_for_model(target)
        similar_actions = similar_actions.filter(target_ct=target_ct, target_id=target.id)

    # Only create a new action if no similar recent action exists
    if not similar_actions.exists():
        Action.objects.create(user=user, verb=verb, target=target)
        return True

    return False
