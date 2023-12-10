#news/forms/py
from django import forms
from django.forms import ModelForm
from .models import NewsStory, Category, Comment

# Choices (from django) is used below to dynamically add new categories to the category dropdown menu.
choices = Category.objects.all().values_list('name', 'name')
choices_list = []
for item in choices:
    choices_list.append(item)

class StoryForm(ModelForm): # new StoryForm class is inheriting from the ModelForm class imported from django.forms
    class Meta:
        model = NewsStory
        fields = ['title', 'tagline', 'author', 'category', 'pub_date', 'image', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control form-item', 'placeholder': 'Enter the film name',}),
            'tagline': forms.TextInput(attrs={'class':'form-control form-item', 'placeholder': 'Describe the film and/or review in a few words',}),
            'pub_date': forms.DateTimeInput(format='%m/%d/%YT%H:%M', attrs={'class':'form-control form-item', 'placeholder':'Select a date', 'type':'datetime-local'}),
            'category': forms.Select(choices=choices_list, attrs={'class':'form-control form-item', 'placeholder':'Select a category'}),
            'image': forms.TextInput(attrs={'class': 'form-control form-item', 'placeholder':'Enter an image URL'}),
            'content': forms.Textarea(attrs={'class': 'form-control form-item', 'placeholder': 'Write your review!'}),
        }

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
          'content': forms.Textarea(attrs={'placeholder':"Share your thoughts about the film and/or review", 'label':'Comment','class':'form-item',}),
    }