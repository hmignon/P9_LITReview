from itertools import chain

from django.contrib.auth.models import User
from django.db.models import CharField, Value

from reviews.models import Review, Ticket
from users.models import UserFollow


def sort_posts(reviews, tickets):
    if not reviews and not tickets:
        posts_list = False
    elif tickets and not reviews:
        posts_list = sorted(tickets, key=lambda post: post.time_created, reverse=True)
    elif reviews and not tickets:
        posts_list = sorted(reviews, key=lambda post: post.time_created, reverse=True)
    else:
        posts_list = sorted(chain(reviews, tickets), key=lambda post: post.time_created, reverse=True)

    return posts_list


def get_user_viewable_reviews(user: User):
    user_reviews = get_user_reviews(user)
    followed_reviews = get_followed_reviews(user)
    unfollowed_reviews = get_unfollowed_reviews(user)

    if user_reviews:
        reviews = chain(user_reviews)
        if followed_reviews:
            reviews = chain(reviews, followed_reviews)
            if unfollowed_reviews:
                reviews = chain(reviews, unfollowed_reviews)
        elif unfollowed_reviews:
            reviews = chain(reviews, unfollowed_reviews)

    elif followed_reviews and not user_reviews:
        reviews = chain(followed_reviews)
        if unfollowed_reviews:
            reviews = chain(reviews, unfollowed_reviews)

    elif unfollowed_reviews and not user_reviews and not followed_reviews:
        reviews = chain(unfollowed_reviews)

    else:
        reviews = False

    return reviews


def get_user_viewable_tickets(user: User):
    user_tickets = get_user_tickets(user)
    followed_tickets = get_followed_tickets(user)

    if user_tickets:
        tickets = chain(user_tickets)
        if followed_tickets:
            tickets = chain(tickets, followed_tickets)

    elif followed_tickets and not user_tickets:
        tickets = chain(followed_tickets)

    else:
        tickets = False

    return tickets


def get_user_reviews(user: User):
    user_reviews = Review.objects.filter(user=user)
    user_reviews = user_reviews.annotate(content_type=Value('REVIEW', CharField()))

    if user_reviews:
        user_reviews = chain(user_reviews)
    else:
        user_reviews = False

    return user_reviews


def get_followed_reviews(user: User):
    user_follows = UserFollow.objects.filter(user=user)
    followed_reviews = Review.objects.none()

    if user_follows:
        for user_follow in user_follows:
            user_follow_review = Review.objects.filter(user=user_follow.followed_user)
            user_follow_review = user_follow_review.annotate(content_type=Value('REVIEW', CharField()))

            followed_reviews = chain(followed_reviews, user_follow_review)

    else:
        followed_reviews = False

    return followed_reviews


def get_unfollowed_reviews(user: User):
    user_follows = UserFollow.objects.filter(user=user)
    user_tickets = Ticket.objects.filter(user=user)
    unfollowed_reviews = Review.objects.none()

    if user_tickets:
        for ticket in user_tickets:
            reviews = Review.objects.filter(ticket=ticket).exclude(user=user)
            reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

            if reviews:
                for user_f in user_follows:
                    reviews = reviews.exclude(user=user_f.followed_user)

                unfollowed_reviews = chain(reviews)

            else:
                unfollowed_reviews = False

    else:
        unfollowed_reviews = False

    return unfollowed_reviews


def get_user_tickets(user: User):
    user_tickets = Ticket.objects.filter(user=user)
    user_tickets = user_tickets.annotate(content_type=Value('TICKET', CharField()))

    if user_tickets:
        user_tickets = chain(user_tickets)
    else:
        user_tickets = False

    return user_tickets


def get_followed_tickets(user: User):
    user_follows = UserFollow.objects.filter(user=user)
    followed_tickets = Ticket.objects.none()

    if user_follows:
        for user_follow in user_follows:
            user_follow_ticket = Ticket.objects.filter(user=user_follow.followed_user)
            user_follow_ticket = user_follow_ticket.annotate(content_type=Value('TICKET', CharField()))

            followed_tickets = chain(followed_tickets, user_follow_ticket)

    else:
        followed_tickets = False

    return followed_tickets
