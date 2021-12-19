from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from PIL import Image, ImageOps


class Ticket(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(default=timezone.now)

    image = models.ImageField(blank=True, null=True, upload_to='reviews_img')

    def __str__(self):
        return self.title

    if image is True:
        def save(self, *args, **kwargs):
            super().save()

            img = ImageOps.contain(
                Image.open(self.image.path),
                (200, 200),
                method=3
            )

            img.save(self.image.path)

    def get_absolute_url(self):
        return reverse('ticket-detail', kwargs={'pk': self.pk})


class Review(models.Model):
    ticket = models.ForeignKey(blank=True, null=True, to=Ticket, on_delete=models.CASCADE)

    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192, blank=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(default=timezone.now)

    image = models.ImageField(blank=True, null=True, upload_to='reviews_img')

    def __str__(self):
        return self.headline

    if image is True:
        def save(self, *args, **kwargs):
            super().save()

            img = ImageOps.contain(
                Image.open(self.image.path),
                (200, 200),
                method=3
            )

            img.save(self.image.path)

    def get_absolute_url(self):
        return reverse('review-detail', kwargs={'pk': self.pk})


class UserFollow(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='following'
    )
    followed_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='followed_by'
    )

    class Meta:
        # ensures we don't get multiple UserFollows instances
        # for unique user-user_followed pairs
        unique_together = ('user', 'followed_user')