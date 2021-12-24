from itertools import chain

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.db.models import Value, CharField
from django.shortcuts import render, redirect
from django.views.generic import DeleteView, DetailView

from .forms import NewReviewForm, NewTicketForm
from .models import Review, Ticket
from .utils import (
    get_user_viewable_reviews,
    get_user_viewable_tickets
)


@login_required
def feed(request):
    reviews = get_user_viewable_reviews(request.user)
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    tickets = get_user_viewable_tickets(request.user)
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    posts_list = sorted(chain(reviews, tickets), key=lambda post: post.time_created, reverse=True)

    if posts_list:
        paginator = Paginator(posts_list, 5)
        page = request.GET.get('page')
        posts = paginator.get_page(page)
    else:
        posts = None

    context = {
        'posts': posts,
        'r_tickets': [],
        'title': 'Feed',
    }

    return render(request, 'reviews/feed.html', context)


@login_required
def my_posts(request):
    reviews = Review.objects.filter(user=request.user)
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    tickets = Ticket.objects.filter(user=request.user)
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

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

    posts_list = sorted(chain(reviews, tickets), key=lambda post: post.time_created, reverse=True)

    if posts_list:
        paginator = Paginator(posts_list, 5)
        page = request.GET.get('page')
        posts = paginator.get_page(page)
        total_posts = paginator.count
    else:
        posts = None
        total_posts = 0

    context = {
        'posts': posts,
        'title': f'My Posts ({total_posts})',
        'r_tickets': replied_tickets,
        'r_reviews': replied_reviews
    }

    return render(request, 'reviews/feed.html', context)


# Reviews
@login_required
def review_new(request):
    if request.method == 'POST':
        t_form = NewTicketForm(request.POST, request.FILES)
        r_form = NewReviewForm(request.POST)

        if t_form.is_valid() and r_form.is_valid():
            t = Ticket.objects.create(
                user=request.user,
                title=request.POST['title'],
                description=request.POST['description'],
                image=request.FILES['image']
            )
            t.save()
            Review.objects.create(
                ticket=t,
                user=request.user,
                headline=request.POST['headline'],
                rating=request.POST['rating'],
                body=request.POST['body']
            )
            messages.success(request, f'Your review has been saved!')
            return redirect('reviews-feed')

    else:
        t_form = NewTicketForm()
        r_form = NewReviewForm()

    context = {
        't_form': t_form,
        'r_form': r_form,
        'title': 'New Review'
    }

    return render(request, 'reviews/review_form.html', context)


@login_required
def review_response(request, pk):
    ticket = Ticket.objects.get(id=pk)

    if request.method == 'POST':
        r_form = NewReviewForm(request.POST)

        if r_form.is_valid():
            Review.objects.create(
                ticket=ticket,
                user=request.user,
                headline=request.POST['headline'],
                rating=request.POST['rating'],
                body=request.POST['body']
            )
            messages.success(request, 'Your response has been saved!')
            return redirect('reviews-feed')

    else:
        r_form = NewReviewForm()

    context = {
        'r_form': r_form,
        'post': ticket,
        'title': 'Response Review'
    }

    return render(request, 'reviews/review_form.html', context)


@login_required
def review_update(request, pk):
    review = Review.objects.get(id=pk)

    if request.method == 'POST':
        r_form = NewReviewForm(request.POST, instance=review)

        if r_form.is_valid():
            r_form.save()
            messages.success(request, f'Your review has been updated!')
            return redirect('reviews-feed')

    else:
        r_form = NewReviewForm(instance=review)

    context = {
        'r_form': r_form,
        'post': review.ticket,
        'title': 'Update Review'
    }

    return render(request, 'reviews/review_form.html', context)


class ReviewDetailView(LoginRequiredMixin, DetailView):
    model = Review
    context_object_name = 'post'


class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    success_url = '/'
    context_object_name = 'post'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False


# Tickets
@login_required
def ticket_new(request):
    if request.method == 'POST':
        form = NewTicketForm(request.POST, request.FILES)

        if form.is_valid():
            image = request.FILES.get('image', None)
            Ticket.objects.create(
                user=request.user,
                title=request.POST['title'],
                description=request.POST['description'],
                image=image
            )
            messages.success(request, 'Your ticket has been saved!')
            return redirect('reviews-feed')

    else:
        form = NewTicketForm()

    context = {
        'form': form,
        'title': 'New Ticket'
    }

    return render(request, 'reviews/ticket_form.html', context)


@login_required
def ticket_update(request, pk):
    ticket = Ticket.objects.get(id=pk)

    if request.method == 'POST':
        form = NewTicketForm(request.POST, request.FILES, instance=ticket)

        if form.is_valid():
            form.save()
            messages.success(request, f'Your ticket has been updated!')
            return redirect('reviews-feed')

    else:
        form = NewTicketForm(instance=ticket)

    context = {
        'form': form,
        'title': 'Update Ticket'
    }

    return render(request, 'reviews/ticket_form.html', context)


class TicketDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ticket
    success_url = '/'
    context_object_name = 'post'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False
