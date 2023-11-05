from django.db import models


class BookOfTheMonth(models.Model):
    """
    Allows admin to publish a blog post about
    a chosen book for the month.
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(
        upload_to='images/', default='default_post_image_vrz129',
        blank=True
    )
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.id} {self.title}'