from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse

class Image(models.Model):
    """
    Model representing an image uploaded by a user.

    Attributes:
        user (ForeignKey): The user who uploaded the image.
        title (CharField): Title of the image.
        slug (SlugField): URL-friendly version of the title. Auto-generated if blank.
        url (URLField): Original URL of the image.
        image (ImageField): Uploaded image file.
        description (TextField): Optional description of the image.
        created (DateField): Date the image was created. Auto-set on creation.
        users_like (ManyToManyField): Users who have liked this image.
        total_likes (PositiveIntegerField): Cached number of likes.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='images_created',
        on_delete=models.CASCADE,
        null=True
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)  # Auto-generated if blank
    url = models.URLField(max_length=2000)
    image = models.ImageField(upload_to='images/%Y/%m/%d/')  # Upload path with date-based folders
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True)
    users_like = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='images_liked',
        blank=True
    )
    total_likes = models.PositiveIntegerField(default=0)

    class Meta:
        # Database indexes to optimize queries by creation date and total likes
        indexes = [
            models.Index(fields=['-created']),
            models.Index(fields=['-total_likes'])
        ]
        # Default ordering by newest first
        ordering = ['-created']

    def __str__(self):
        """String representation of the model."""
        return self.title

    def save(self, *args, **kwargs):
        """
        Override save method to automatically generate a slug from the title
        if it's not provided.
        """
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """
        Return the URL to access a particular image instance.
        This is used in templates and views to create links to image details.
        """
        return reverse("images:detail", args=[self.id, self.slug])
