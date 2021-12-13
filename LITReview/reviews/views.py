from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Post


@login_required
def feed(request):
    context = {
        'posts': Post.objects.all(),
        'title': 'Feed'
    }
    return render(request, 'reviews/feed.html', context)


@login_required
def posts(request):
    return render(request, 'reviews/posts.html', {'title': 'Posts'})


@login_required
def subscriptions(request):
    return render(request, 'reviews/subscriptions.html', {'title': 'Subscriptions'})
