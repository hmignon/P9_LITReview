from PIL import Image, ImageOps
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    image = models.ImageField(default="default.jpg", upload_to="profile_pics")
    location = models.CharField(max_length=64, blank=True)
    bio = models.TextField(max_length=2048, blank=True)
    display_real_name = models.BooleanField(default=False)
    display_location = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super().save()
        img = ImageOps.fit(
            Image.open(self.image.path), (300, 300), method=3, centering=(0.5, 0.5)
        )
        img.save(self.image.path)


class UserFollow(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="following"
    )
    followed_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="followed_by",
    )

    def __str__(self):
        return f"{self.user.username} -> {self.followed_user.username}"

    class Meta:
        unique_together = ("user", "followed_user")
