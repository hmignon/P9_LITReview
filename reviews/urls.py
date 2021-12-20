from django.urls import path
from .views import (
    ReviewNewView,
    TicketNewView,
    ReviewUpdateView,
    ReviewDeleteView,
    UnsubscribeView,
    TicketUpdateView,
    TicketDeleteView
)
from . import views

urlpatterns = [
    path('', views.feed, name='reviews-feed'),
    path('my_posts/', views.my_posts, name='user-posts'),
    path('review/new/', ReviewNewView.as_view(), name='review-new'),
    path('review/<int:pk>/update/', ReviewUpdateView.as_view(), name='review-update'),
    path('review/<int:pk>/delete/', ReviewDeleteView.as_view(), name='review-delete'),
    path('ticket/new/', TicketNewView.as_view(), name='ticket-new'),
    path('ticket/<int:pk>/update/', TicketUpdateView.as_view(), name='ticket-update'),
    path('ticket/<int:pk>/delete/', TicketDeleteView.as_view(), name='ticket-delete'),
    path('subscriptions/', views.subscriptions, name='reviews-subs'),
    path('subscriptions/confirm_unsub', UnsubscribeView.as_view(), name='confirm-unsub')
]
