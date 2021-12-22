from django.db import models
from django.conf import settings
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
        return f'Ticket-{self.id} ({self.title})'

    if image is True:
        def save(self, *args, **kwargs):
            super().save()

            img = ImageOps.contain(
                Image.open(self.image.path),
                (200, 200),
                method=3
            )

            img.save(self.image.path)


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
        return f'Review-{self.id} ({self.headline})'

    if image is True:
        def save(self, *args, **kwargs):
            super().save()

            img = ImageOps.contain(
                Image.open(self.image.path),
                (200, 200),
                method=3
            )

            img.save(self.image.path)
