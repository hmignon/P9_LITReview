from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.views.generic import DeleteView

from .forms import (
    UserRegisterForm,
    UserUpdateForm,
    ProfileUpdateForm,
    SubscribeForm,
)
from .models import UserFollow


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, f"Your account has been created! You are now able to log in."
            )
            return redirect("login")

    else:
        form = UserRegisterForm()

    return render(request, "users/register.html", {"form": form})


@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Your account has been updated!")
            return redirect("profile")

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {"u_form": u_form, "p_form": p_form, "title": "Profile"}

    return render(request, "users/profile.html", context)


@login_required
def subscriptions(request):
    if request.method == "POST":
        form = SubscribeForm(request.POST)

        if form.is_valid():
            try:
                followed_user = User.objects.get(username=request.POST["followed_user"])
                if request.user == followed_user:
                    messages.error(request, "You can't subscribe to yourself!")
                else:
                    try:
                        UserFollow.objects.create(
                            user=request.user, followed_user=followed_user
                        )
                        messages.success(
                            request, f"You are now following {followed_user}!"
                        )
                    except IntegrityError:
                        messages.error(
                            request, f"You are already following {followed_user}!"
                        )

            except User.DoesNotExist:
                messages.error(
                    request, f'The user {form.data["followed_user"]} does not exist.'
                )

    else:
        form = SubscribeForm()

    user_follows = UserFollow.objects.filter(user=request.user).order_by(
        "followed_user"
    )
    followed_by = UserFollow.objects.filter(followed_user=request.user).order_by("user")

    context = {
        "form": form,
        "user_follows": user_follows,
        "followed_by": followed_by,
        "title": "Subscriptions",
    }

    return render(request, "users/subscriptions.html", context)


class UnsubscribeView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = UserFollow
    success_url = "/subscriptions"
    context_object_name = "unsub"

    def test_func(self):
        unsub = self.get_object()
        if self.request.user == unsub.user:
            return True
        return False

    def delete(self, request, *args, **kwargs):
        messages.warning(
            self.request,
            f"You have stopped following {self.get_object().followed_user}.",
        )
        return super(UnsubscribeView, self).delete(request, *args, **kwargs)
