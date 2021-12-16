from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Review


class ReviewListView(LoginRequiredMixin, ListView):
    model = Review
    template_name = 'reviews/feed.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']


class ReviewDetailView(LoginRequiredMixin, DetailView):
    model = Review


class ReviewNewView(LoginRequiredMixin, CreateView):
    model = Review
    fields = ['headline', 'rating', 'body', 'image']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    fields = ['headline', 'rating', 'body', 'image']

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


@login_required
def posts(request):
    return render(request, 'reviews/posts.html', {'title': 'Posts'})


@login_required
def subscriptions(request):
    return render(request, 'reviews/subscriptions.html', {'title': 'Subscriptions'})
