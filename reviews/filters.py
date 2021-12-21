from itertools import chain

from django.contrib.auth.models import User
from django.db.models import CharField, Value

from reviews.models import Review, Ticket
from users.models import UserFollow


def get_users_viewable_reviews(user: User):
    user_reviews = Review.objects.filter(user=user)
    user_reviews = user_reviews.annotate(content_type=Value('REVIEW', CharField()))

    return user_reviews


def get_users_viewable_tickets(user: User):
    user_tickets = Ticket.objects.filter(user=user)
    user_tickets = user_tickets.annotate(content_type=Value('TICKET', CharField()))

    return user_tickets


def get_followed_reviews(user: User):
    user_follows = UserFollow.objects.filter(user=user)
    followed_reviews = Review.objects.none()

    for user_follow in user_follows:
        user_follow_review = Review.objects.filter(user=user_follow.followed_user)
        user_follow_review = user_follow_review.annotate(content_type=Value('REVIEW', CharField()))

        followed_reviews = chain(followed_reviews, user_follow_review)

    return followed_reviews


def get_followed_tickets(user: User):
    user_follows = UserFollow.objects.filter(user=user)
    followed_tickets = Ticket.objects.none()

    for user_follow in user_follows:
        user_follow_ticket = Ticket.objects.filter(user=user_follow.followed_user)
        user_follow_ticket = user_follow_ticket.annotate(content_type=Value('TICKET', CharField()))

        followed_tickets = chain(followed_tickets, user_follow_ticket)

    return followed_tickets
