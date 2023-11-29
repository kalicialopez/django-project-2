from django.views import generic
from django.urls import reverse_lazy
from .models import NewsStory
from .forms import StoryForm


class IndexView(generic.ListView):
    template_name = 'news/index.html'
    context_object_name = "all_stories"

    def get_queryset(self):
        '''Return all news stories.'''
        return NewsStory.objects.all().order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_stories'] = NewsStory.objects.all().order_by('-pub_date')[:4]
        return context

class StoryView(generic.DetailView):
    model = NewsStory
    template_name = 'news/story.html'
    context_object_name = "story"

class AddStoryView(generic.CreateView): # CreateView is a generic view that allows us to create a new object. Our subclass AddStoryView inherits from this base view.
    form_class = StoryForm # what form is used for the AddStoryView
    context_object_name = 'storyform' # what variable name should be used to store that form under in the template
    template_name = 'news/createStory.html' # which template the view should use
    success_url = reverse_lazy('news:index') # where the user should be redirected to after successfully submitting the form