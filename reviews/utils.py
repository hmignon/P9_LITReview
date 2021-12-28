from django.contrib.auth.models import User

from reviews.models import Review, Ticket
from users.models import UserFollow


def get_user_viewable_reviews(user: User):
    """
    All viewable reviews for user feed:
    Reviews by followed users + current user
    Reviews to current user tickets if review author is not followed

    @param user: currently logged-in User instance
    @return: filtered reviews queryset with no duplicate results
    """
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

    reviews = Review.objects.filter(id__in=reviews).distinct()

    return reviews


def get_user_viewable_tickets(user: User):
    """
    All viewable tickets for user feed:
    Tickets by followed users + current user
    Filter out tickets with review response

    @param user: currently logged-in User instance
    @return: filtered tickets queryset
    """
    user_follows = UserFollow.objects.filter(user=user)
    followers = [user]
    for follow in user_follows:
        followers.append(follow.followed_user)

    tickets = Ticket.objects.filter(user__in=followers)
    for ticket in tickets:
        replied = Review.objects.filter(ticket=ticket)
        if replied:
            tickets = tickets.exclude(id=ticket.id)

    return tickets


def get_replied_tickets(tickets):
    """
    Filter out tickets with review response for 'my posts' and 'user posts'
    Get corresponding review to link to for detail view

    @param tickets: user tickets queryset
    @return: list of tickets with response, list of review responses to corresponding tickets
    """
    replied_tickets = []
    replied_reviews = []

    for ticket in tickets:
        try:
            replied = Review.objects.get(ticket=ticket)
            if replied:
                replied_tickets.append(replied.ticket)
                replied_reviews.append(replied)

        except Review.DoesNotExist:
            pass

    return replied_tickets, replied_reviews


def get_user_follows(user):
    """Returns list of users followed by current user"""
    follows = UserFollow.objects.filter(user=user)
    followed_users = []
    for follow in follows:
        followed_users.append(follow.followed_user)

    return followed_users
