from django.urls import path

from . import views
from .views import (
    ReviewDeleteView,
    TicketDeleteView,
)

app_name = "reviews"
urlpatterns = [
    path("", views.feed, name="feed"),
    path("my_posts/", views.user_posts, name="myposts"),
    path("user_posts/<int:pk>/", views.user_posts, name="userposts"),
    path("review/new/", views.review_new, name="new"),
    path("reviews/response/<int:pk>", views.review_response, name="response"),
    path("review/<int:pk>/update/", views.review_update, name="update"),
    path("review/<int:pk>/detail", views.review_detail, name="detail"),
    path("review/<int:pk>/delete/", ReviewDeleteView.as_view(), name="delete"),
    path("ticket/new/", views.ticket_new, name="ticket-new"),
    path("ticket/<int:pk>/update/", views.ticket_update, name="ticket-update"),
    path("ticket/<int:pk>/detail", views.ticket_detail, name="ticket-detail"),
    path("ticket/<int:pk>/delete/", TicketDeleteView.as_view(), name="ticket-delete"),
]
