from django.forms import ModelForm
from weekend.common.models import Review

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        exclude = ('user',)
