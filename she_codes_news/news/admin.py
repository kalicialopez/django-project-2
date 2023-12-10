from django.contrib import admin

from .forms import StoryForm
from .models import NewsStory, Category, Comment

admin.site.register(NewsStory)
admin.site.register(Category)
admin.site.register(Comment) 
