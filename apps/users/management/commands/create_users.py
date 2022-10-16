import uuid
from random import randint, choice

import requests
from django.core.management import BaseCommand
from faker import Faker
from tqdm import trange

from apps.users.models import User, UserFollow


class Command(BaseCommand):
    help = "Create sample users."
    image_storage_path = "media/profile_pics/"
    fake = Faker()

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            "-n",
            dest="number",
            default=15,
            type=int,
            help="Specify the number of users to create.",
        )

    def handle(self, *args, **options):
        number = options["number"]
        self.stdout.write(f"Creating {number} user(s)...")
        for _ in trange(number):
            user = self.create_users()
            self.create_followers(user)
        self.stdout.write(f"Successfully created {number} user(s).")

    def create_users(self):
        user = User.objects.create_user(
            first_name=self.fake.first_name(),
            last_name=self.fake.last_name(),
            username=f"{self.fake.user_name()}{randint(1, 99)}",
            password=self.fake.password(length=8),
            email=self.fake.ascii_safe_email(),
            image=self.download_image(),
            bio=self.fake.paragraph(nb_sentences=randint(10, 20)),
            location=f"{self.fake.city()}, {self.fake.country()}",
            display_real_name=self.fake.boolean(chance_of_getting_true=50),
            display_location=self.fake.boolean(chance_of_getting_true=50),
        )
        return user

    def download_image(self):
        with_image = self.fake.boolean(chance_of_getting_true=90)
        if with_image:
            image = requests.get("https://picsum.photos/300")
            image_path = f"{self.image_storage_path}{str(uuid.uuid4())}.jpeg"
            with open(image_path, "wb") as f:
                f.write(image.content)

            return image_path.replace("media/", "")

        return "default.jpg"

    @staticmethod
    def create_followers(user):
        users = User.objects.exclude(id=user.id)
        for i in range(randint(1, users.count() + 1)):
            follow = choice(users)
            if bool(follow):
                try:
                    follow = UserFollow.objects.get(user=user, followed_user=follow)
                except UserFollow.DoesNotExist:
                    UserFollow.objects.create(user=user, followed_user=follow)
