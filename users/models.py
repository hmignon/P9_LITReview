from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from PIL import Image, ImageOps


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save()

        img = ImageOps.fit(
            Image.open(self.image.path),
            (300, 300),
            method=3,
            centering=(0.5, 0.5)
        )

        img.save(self.image.path)


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

    def __str__(self):
        return f"{self.user.username} -> {self.followed_user.username}"

    class Meta:
        unique_together = ('user', 'followed_user')
