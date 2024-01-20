from stripe import Review
from app1.models import ProductReview
from django import forms  # Import the 'forms' module from Django

class ProductReviewForm(forms.ModelForm):  # Corrected class definition
    review = forms.CharField(widget=forms.Textarea(attrs={'placeholder': "Write a review"}))

    class Meta:
        model = ProductReview
        fields = ['review', 'rating']

from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Full Name"}))
    bio = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Bio"}))
    phone = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Phone"}))

    class Meta:
        model = Profile
        fields = ['full_name', 'image', 'bio', 'phone']
