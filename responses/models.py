from django.db import models
from django.contrib.auth.models import User
from bookclubevents.models import BookClubEvent


class Response(models.Model):
    """
    Response model, related to BookClubEvents
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    bookclubevent = models.ForeignKey(
        BookClubEvent, on_delete=models.CASCADE, related_name='responses'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['owner', 'bookclubevent']

    def __str__(self):
        return f'{self.owner} {self.bookclubevent}'
