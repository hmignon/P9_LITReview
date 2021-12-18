from django.urls import path
from .views import (
    ReviewDetailView,
    ReviewUpdateView,
    ReviewDeleteView,
    UserPostListView,
    TicketDetailView
)
from . import views

urlpatterns = [
    path('', views.feed, name='reviews-feed'),
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    path('review/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
    path('review/new/', views.new_review, name='review-new'),
    path('review/<int:pk>/update/', ReviewUpdateView.as_view(), name='review-update'),
    path('review/<int:pk>/delete/', ReviewDeleteView.as_view(), name='review-delete'),
    path('ticket/<int:pk>/', TicketDetailView.as_view(), name='ticket-detail'),
    path('ticket/new/', views.new_ticket, name='ticket-new'),
    # path('ticket/<int:pk>/update/', PostUpdateView.as_view(), name='ticket-update'),
    # path('ticket/<int:pk>/delete/', PostDeleteView.as_view(), name='ticket-delete'),
    path('subscriptions/', views.subscriptions, name='reviews-subs'),
    path('posts/', views.posts, name="reviews-posts")
]
