from django import forms
from .models import Movie, Review

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ('title', 'description', 'genre',)

class ReviewForm(forms.ModelForm):
    score = forms.FloatField(
        max_value = 5,
        min_value = 0,
        widget=forms.NumberInput(
            attrs = {
                "step":"0.5",
            }
        )
    )
    
    class Meta:
        model = Review
        fields = ('content', 'score',)