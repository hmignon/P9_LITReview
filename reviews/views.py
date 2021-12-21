# TODO review in response to ticket

from itertools import chain

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView
)

from .filters import (
    get_users_viewable_reviews,
    get_followed_reviews,
    get_users_viewable_tickets,
    get_followed_tickets
)
from .forms import NewReviewForm, NewTicketForm
from .models import Review, Ticket


@login_required
def feed(request):
    reviews = chain(
        get_users_viewable_reviews(request.user),
        get_followed_reviews(request.user)
    )

    tickets = chain(
        get_users_viewable_tickets(request.user),
        get_followed_tickets(request.user)
    )

    posts_list = sorted(chain(reviews, tickets), key=lambda post: post.time_created, reverse=True)

    paginator = Paginator(posts_list, 5)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    context = {
        'posts': posts,
        'title': 'Feed',
    }

    return render(request, 'reviews/feed.html', context)


@login_required
def my_posts(request):
    reviews = get_users_viewable_reviews(request.user)
    tickets = get_users_viewable_tickets(request.user)

    posts_list = sorted(chain(reviews, tickets), key=lambda post: post.time_created, reverse=True)

    paginator = Paginator(posts_list, 5)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    context = {
        'posts': posts,
        'title': f'My Posts ({paginator.count})',
    }

    return render(request, 'reviews/feed.html', context)


# Reviews #
class ReviewNewView(LoginRequiredMixin, CreateView):
    model = Review
    template_name = 'reviews/post_form.html'
    form_class = NewReviewForm
    success_url = '/'
    context_object_name = 'post'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    template_name = 'reviews/post_form.html'
    form_class = NewReviewForm
    success_url = '/'
    context_object_name = 'review'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False


class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    success_url = '/'
    context_object_name = 'post'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False


# Tickets #
class TicketNewView(LoginRequiredMixin, CreateView):
    model = Ticket
    template_name = 'reviews/post_form.html'
    form_class = NewTicketForm
    success_url = '/'
    context_object_name = 'post'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TicketUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ticket
    template_name = 'reviews/post_form.html'
    form_class = NewTicketForm
    success_url = '/'
    context_object_name = 'ticket'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False


class TicketDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ticket
    success_url = '/'
    context_object_name = 'post'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False
