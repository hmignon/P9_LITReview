import uuid
from random import choice, randint

import requests
from django.core.management import BaseCommand
from faker import Faker
from tqdm import trange

from apps.reviews.models import Ticket, Review
from apps.reviews.utils import get_replied_tickets
from apps.users.models import User


class Command(BaseCommand):
    help = "Create dummy reviews."
    image_storage_path = "media/reviews_img/"
    users = User.objects.all()
    fake = Faker()

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            "-n",
            dest="number",
            default=25,
            type=int,
            help="Specify the number of reviews to create.",
        )

    def handle(self, *args, **options):
        number = options["number"]
        self.stdout.write(f"Creating {number} review(s)...")
        for _ in trange(number):
            self.create_reviews()

    def create_reviews(self):
        headline = ""
        for i in range(randint(2, 10)):
            headline = f"{headline} {self.fake.word().title()}"

        Review.objects.create(
            ticket=self.check_for_tickets(),
            rating=randint(1, 5),
            headline=headline,
            body=self.fake.paragraph(nb_sentences=randint(20, 40)),
            user=choice(self.users),
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

    def check_for_tickets(self):
        tickets = Ticket.objects.all()
        title = ""
        for i in range(randint(2, 10)):
            title = f"{title} {self.fake.word().title()}"

        replied_tickets, replied_reviews = get_replied_tickets(tickets)
        available_tickets = [t for t in tickets if t not in replied_tickets]

        if not available_tickets:
            ticket = Ticket.objects.create(
                title=title,
                description=self.fake.paragraph(nb_sentences=randint(10, 20)),
                user=choice(self.users),
                image=self.download_image(),
            )
        else:
            ticket = choice(available_tickets)

        return ticket
