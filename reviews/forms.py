from .models import Review, Ticket

from django import forms


class NewReviewForm(forms.ModelForm):
    headline = forms.CharField(
        label="Title",
        max_length=128,
        widget=forms.TextInput(),
        error_messages={'required': 'Please enter a title.'}
    )
    rating = forms.ChoiceField(
        label="Rating",
        widget=forms.RadioSelect(),
        choices=[(str(x+1), x+1) for x in range(5)],
        error_messages={'required': 'Please enter a rating.'}
    )
    body = forms.CharField(
        label="Review",
        max_length=8192,
        widget=forms.Textarea(),
        required=False
    )
    image = forms.ImageField(
        label="Image",
        required=False
    )

    class Meta:
        model = Review
        fields = ['headline', 'rating', 'body', 'image']


class NewTicketForm(forms.ModelForm):
    title = forms.CharField(
        label="Title",
        max_length=128,
        widget=forms.TextInput(),
        error_messages={'required': 'Please enter a title.'}
    )
    description = forms.CharField(
        label="Description",
        max_length=2048,
        widget=forms.Textarea(),
        required=False
    )
    image = forms.ImageField(
        label="Image",
        required=False
    )

    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']