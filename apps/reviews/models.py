from PIL import Image, ImageOps
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class Ticket(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(default=timezone.now)

    image = models.ImageField(blank=True, null=True, upload_to="reviews_img")

    def __str__(self):
        return f"Ticket-{self.title}"

    if image is True:
        def save(self, *args, **kwargs):
            super().save()
            img = ImageOps.contain(Image.open(self.image.path), (200, 200), method=3)
            img.save(self.image.path)


class Review(models.Model):
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Review-{self.headline}"
