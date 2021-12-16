from django.db import models
from django.conf import settings
# from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.utils import timezone
from PIL import Image, ImageOps

"""
class Ticket(models.Model):
    title = models.CharField(max_length=128)
    content = models.TextField(max_length=8192, blank=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)

    image = models.ImageField(default='default.jpg', upload_to='reviews_img')

    def __str__(self):
        return self.title

    def save(self):
        super().save()
        img = Image.open(self.image.path)
        img.save(self.image.path)

    def get_absolute_url(self):
        return reverse('ticket-detail', kwargs={'pk': self.pk})
"""


class Review(models.Model):
    # ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    class Rating(models.IntegerChoices):
        ONE = (1, '1')
        TWO = (2, '2')
        THREE = (3, '3')
        FOUR = (4, '4')
        FIVE = (5, '5')

    rating = models.IntegerField(choices=Rating.choices)

    # rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192, blank=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)

    image = models.ImageField(upload_to='reviews_img')

    def __str__(self):
        return self.headline

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


"""
class UserFollows(models.Model):
    # Your UserFollows model definition goes here

    class Meta:
        # ensures we don't get multiple UserFollows instances
        # for unique user-user_followed pairs
        unique_together = ('user', 'followed_user', )
"""
