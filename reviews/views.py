# TODO image not saving ticket and review (new and update)
# TODO title on review form page

from itertools import chain

from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import CharField, Value
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Review, Ticket
from .forms import NewReviewForm, NewTicketForm


@login_required
def feed(request):
    reviews = get_users_viewable_reviews(request.user)
    tickets = get_users_viewable_tickets(request.user)

    posts = sorted(chain(reviews, tickets), key=lambda post: post.time_created, reverse=True)

    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'posts': posts,
        'title': 'Feed',
        'page_obj': page_obj
    }

    return render(request, 'reviews/feed.html', context)


def get_users_viewable_reviews(user: User):
    # TODO add followed reviews
    user_reviews = Review.objects.filter(user=user)
    user_reviews = user_reviews.annotate(content_type=Value('REVIEW', CharField()))

    return user_reviews


def get_users_viewable_tickets(user: User):
    # TODO add followed tickets
    user_tickets = Ticket.objects.filter(user=user)
    user_tickets = user_tickets.annotate(content_type=Value('TICKET', CharField()))

    return user_tickets


"""
class ReviewListView(LoginRequiredMixin, ListView):
    model = Review
    template_name = 'reviews/feed.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5
"""


def new_ticket(request):
    if request.method == 'POST':
        form = NewTicketForm(request.POST)
        if form.is_valid():
            form.save(request)
            form.instance.user = request.user
            title = form.cleaned_data.get('title')
            messages.success(request, f'Your ticket {title} has been created!')
            return redirect('reviews-feed')

    else:
        form = NewTicketForm()

    context = {
        'form': form,
        'title': 'New Ticket',
    }

    return render(request, 'reviews/review_form.html', context)


class UserPostListView(ListView):
    model = Review
    template_name = 'reviews/posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Review.objects.filter(user=user).order_by('-time_created')


class TicketNewView(LoginRequiredMixin, CreateView):
    model = Ticket
    template_name = 'reviews/review_form.html'
    form_class = NewTicketForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ReviewDetailView(LoginRequiredMixin, DetailView):
    model = Review


class ReviewNewView(LoginRequiredMixin, CreateView):
    model = Review
    template_name = 'reviews/review_form.html'
    form_class = NewReviewForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    template_name = 'reviews/review_form.html'
    form_class = NewReviewForm

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

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False


class TicketDetailView(LoginRequiredMixin, DetailView):
    model = Ticket


@login_required
def posts(request):
    return render(request, 'reviews/posts.html', {'title': 'Posts'})


@login_required
def subscriptions(request):
    return render(request, 'reviews/subscriptions.html', {'title': 'Subscriptions'})
