#news/forms/py
from django import forms
from django.forms import ModelForm
from .models import NewsStory

class StoryForm(ModelForm): # new StoryForm class is inheriting from the ModelForm class imported from django.forms
    class Meta:
        model = NewsStory # we're telling the form that it's going to be used to create a NewsStory object
        fields = ['title', 'author', 'content'] # we're telling the form which fields to include
        widgets = {
            'pub_date': forms.DateInput(
                format='%m/%d/%Y',
                attrs={
                    'class':'form-control',
                    'placeholder':'Select a date',
                    'type':'date'
                }
            ),
        }
