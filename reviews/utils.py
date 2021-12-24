from django.contrib.auth.models import User

from reviews.models import Review, Ticket
from users.models import UserFollow


def get_user_viewable_reviews(user: User):
    user_follows = UserFollow.objects.filter(user=user)
    followers = [user]
    for follow in user_follows:
        followers.append(follow.followed_user)

    reviews = []
    all_reviews = Review.objects.filter(user__in=followers).distinct()
    for review in all_reviews:
        reviews.append(review.id)

    user_tickets = Ticket.objects.filter(user=user)
    for ticket in user_tickets:
        review_responses = Review.objects.filter(ticket=ticket)
        for review in review_responses:
            reviews.append(review.id)

    return Review.objects.filter(id__in=reviews).distinct()


def get_user_viewable_tickets(user: User):
    user_follows = UserFollow.objects.filter(user=user)
    followers = [user]
    for follow in user_follows:
        followers.append(follow.followed_user)

    return Ticket.objects.filter(user__in=followers)
