from django.urls import path
from .views import (
    ReviewDeleteView,
    TicketDeleteView,
    ReviewDetailView
)
from . import views

urlpatterns = [
    path('', views.feed, name='reviews-feed'),
    path('my_posts/', views.my_posts, name='user-posts'),
    path('review/new/', views.review_new, name='review-new'),
    path('reviews/response/<int:pk>', views.review_response, name='response-review'),
    path('review/<int:pk>/update/', views.review_update, name='review-update'),
    path('review/<int:pk>/detail', ReviewDetailView.as_view(), name='review-detail'),
    path('review/<int:pk>/delete/', ReviewDeleteView.as_view(), name='review-delete'),
    path('ticket/new/', views.ticket_new, name='ticket-new'),
    path('ticket/<int:pk>/update/', views.ticket_update, name='ticket-update'),
    path('ticket/<int:pk>/delete/', TicketDeleteView.as_view(), name='ticket-delete')
]
