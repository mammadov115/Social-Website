from django import forms
from .models import Image
from django.core.files.base import ContentFile
from django.utils.text import slugify
import requests

class ImageCreateForm(forms.ModelForm):
    """
    Form for creating a new Image instance by providing a title, URL, and description.
    Downloads the image from the given URL and saves it to the ImageField.
    """

    class Meta:
        model = Image
        fields = ['title', 'url', 'description']
        widgets = {
            # Hide the URL input in the form (can be provided via JS or hidden field)
            'url': forms.HiddenInput
        }

    def clean_url(self):
        """
        Validate that the URL points to an image with a valid extension.
        Raises ValidationError if the extension is not allowed.
        """
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg', 'png']
        extension = url.rsplit('.', 1)[1].lower()  # Extract extension from URL
        if extension not in valid_extensions:
            raise forms.ValidationError('The given URL does not match valid image formats (jpg, jpeg, png).')
        return url

    def save(self, force_insert=False, force_update=False, commit=True):
        """
        Override save method to:
            - Download the image from the provided URL
            - Save it to the model's ImageField
            - Optionally commit to the database
        """
        # Get the unsaved Image instance
        image = super().save(commit=False)
        image_url = self.cleaned_data['url']
        name = slugify(image.title)  # Make filename URL-friendly
        extension = image_url.rsplit('.', 1)[1].lower()
        image_name = f'{name}.{extension}'

        # Download the image from the given URL
        response = requests.get(image_url)
        # Save the downloaded content to the ImageField without committing yet
        image.image.save(image_name, ContentFile(response.content), save=False)

        if commit:
            # Save the model instance to the database
            image.save()

        return image
