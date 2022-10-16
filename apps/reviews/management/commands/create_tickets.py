import uuid
from random import choice, randint

import requests
from django.core.management import BaseCommand
from faker import Faker
from tqdm import trange

from apps.reviews.models import Ticket
from apps.users.models import User


class Command(BaseCommand):
    help = "Create dummy tickets."
    image_storage_path = "media/reviews_img/"
    fake = Faker()

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            "-n",
            dest="number",
            default=25,
            type=int,
            help="Specify the number of tickets to create.",
        )

    def handle(self, *args, **options):
        number = options["number"]
        self.stdout.write(f"Creating {number} review(s)...")
        for _ in trange(number):
            self.create_tickets()

    def create_tickets(self):
        users = User.objects.all()
        title = ""

        for i in range(randint(2, 10)):
            title = f"{title} {self.fake.word().title()}"

        Ticket.objects.create(
            title=title,
            description=self.fake.paragraph(nb_sentences=randint(10, 20)),
            user=choice(users),
            image=self.download_image(),
        )

    def download_image(self):
        with_image = self.fake.boolean(chance_of_getting_true=80)
        if with_image:
            image = requests.get("https://picsum.photos/200/300")
            image_path = f"{self.image_storage_path}{str(uuid.uuid4())}.jpeg"
            with open(image_path, "wb") as f:
                f.write(image.content)

            return image_path.replace("media/", "")

        return None
