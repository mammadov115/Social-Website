from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Action(models.Model):
    """
    Represents an action performed by a user for activity streams.

    Example: "John liked a post" or "Alice is following Bob".

    Fields:
    - user: the actor performing the action
    - verb: short description of the action
    - created: timestamp when action was created
    - target_ct: content type of the target object (optional)
    - target_id: primary key of the target object (optional)
    - target: generic foreign key to any model instance (optional)
    """
    user = models.ForeignKey(
        'auth.User',
        related_name='actions',
        on_delete=models.CASCADE
    )
    verb = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    # Generic relation to target object
    target_ct = models.ForeignKey(
        ContentType,
        blank=True,
        null=True,
        related_name='target_obj',
        on_delete=models.CASCADE
    )
    target_id = models.PositiveIntegerField(blank=True, null=True)
    target = GenericForeignKey('target_ct', 'target_id')

    class Meta:
        """
        Meta options:
        - Indexes: for fast querying by created date and target object
        - Ordering: newest actions first
        """
        indexes = [
            models.Index(fields=['-created']),            # Optimize queries by creation date
            models.Index(fields=['target_ct', 'target_id'])  # Optimize queries by target object
        ]
        ordering = ['-created']

    def __str__(self):
        """
        Example: "John liked a post" or "Alice is following Bob"
        """
        return f"{self.user} {self.verb}"
