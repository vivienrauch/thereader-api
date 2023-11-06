from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.utils import timezone


class BookClubEvent(models.Model):
    """
    BookClubEvent model, related to 'owner', i.e. a User instance.
    Default image set so that we can always reference image.url.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    event_name = models.CharField(max_length=255)
    event_description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date = models.DateField(default=date.today)
    event_organiser = models.CharField(max_length=255, blank=True)
    event_location = models.TextField(blank=True)
    event_start = models.TimeField(default=timezone.now)
    event_end = models.TimeField(default=timezone.now)
    contact = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    event_cover = models.ImageField(
        upload_to='images/', default='../default_post_image_vrz129', blank=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.id} {self.name}'

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.id} {self.name}'