from django.contrib.auth.models import User
from django.db import models
# Create your models here.
from django.utils import timezone

from blog.models import Article


class Comment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    content = models.TextField()
    created = models.DateTimeField(default=timezone.now)

    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='children'
    )

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.content[:20]
