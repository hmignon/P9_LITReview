from django.urls import path
from . import views


urlpatterns = [
    path('', views.feed, name='reviews-feed'),
    path('subscriptions/', views.subscriptions, name='reviews-subs'),
    path('posts/', views.posts, name="reviews-posts")
]
