from django.forms import ModelForm
from weekend.models import Review

class ReviewForm(ModelForm):
    class Meta:
        model = Review
