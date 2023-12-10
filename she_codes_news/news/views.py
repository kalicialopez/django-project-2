# news/views.py

from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect

from .models import Category, NewsStory, Comment 
from .forms import StoryForm, CommentForm

from users.urls import urlpatterns
from users.models import CustomUser

from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.auth.decorators import login_required
# from django.utils.decorators import method_decorator


class IndexView(generic.ListView):
    template_name = 'news/index.html'
    context_object_name = "all_stories"

    def get_queryset(self):
        '''Return all news stories.'''
        return NewsStory.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_stories'] = NewsStory.objects.all().order_by('-pub_date')[:4]
        return context


# ==================== STORIES ==================== #

class StoryView(generic.DetailView):
    model = NewsStory
    template_name = 'news/story.html'
    context_object_name = "story"
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['form'] = CommentForm
        # context = ['form'] = CommentForm
        # context = {'form': CommentForm}
        context['comments'] = Comment.objects.order_by('-pub_date')
        return context

    # def post(self, request, *args, **kwargs):
    #     form = CommentForm(request.POST)
    #     if form.is_valid():
    #         if request.user.is_authenticated:
    #             return HttpResponseRedirect(reverse('add_comment', kwargs={'pk': self.kwargs.get("pk")}))
    #         else:
    #             request.session['comment_form_data'] = request.POST
    #             request.session['story_pk'] = self.kwargs.get("pk")
    #             return redirect('/login/')

# ----------- ADD STORY ----------- #

class AddStoryView(LoginRequiredMixin,generic.CreateView): # CreateView is a generic view that allows us to create a new object. Our subclass AddStoryView inherits from this base view.
    form_class = StoryForm # what form is used for the AddStoryView
    context_object_name = 'storyform' # variable name used in the template to access the object that this view is operating upon 
    template_name = 'news/createStory.html' # which template the view should use
    success_url = reverse_lazy('news:index') # where the user should be redirected to after successfully submitting the form
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['add_story_view'] = True # Required as I am also using the createStory template to edit the story. Used in template to conditionally render different parts of the template, depending on what the use is doing (adding a story or editing their story)
        return context
 
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
# ---------- EDIT STORY ---------- #   
class EditStoryView(LoginRequiredMixin, generic.edit.UpdateView):
    form_class = StoryForm
    model = NewsStory
    context_object_name = 'storyForm'
    template_name = 'news/createStory.html'
    success_url = reverse_lazy('news:newsStory')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['add_story_view'] = False # Required because I am using the same template to edit a story. Set to false and used in the template to conditionally render different parts of it, based on the action of the user. 
        return context
 
# ---------- DELETE STORY ---------- #
def delete_success_view(request):
    return render(request, 'news/deleteSuccess.html')
      
class DeleteStoryView(LoginRequiredMixin, generic.edit.DeleteView):
    model = NewsStory
    template_name = 'news/deleteView.html'
    success_url = reverse_lazy('news:deleteSuccess')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['story'] = NewsStory.objects.get(id=self.kwargs['pk'])
        return context


# ==================== COMMENTS ==================== #

class CommentView(generic.DetailView):
    model = Comment
    template_name = 'news/comment.html'
    context_object_name = "comment"

# ----------- ADD COMMENT ----------- #

class AddCommentView(LoginRequiredMixin, generic.CreateView):
    form_class = CommentForm
    template_name = 'news/createComment.html'
    context_object_name = 'comments'
    
    # def get(self, request, *args, **kwargs):
    #     if 'comment_form_data' in request.session and 'story_pk' in request.session:
    #         form_data = request.session.pop('comment_form_data')
    #         story_pk = request.session.pop('story_pk')
    #         form = CommentForm(form_data)
    #         if form.is_valid():
    #             form.instance.author = request.user
    #             story = get_object_or_404(NewsStory, pk=story_pk)
    #             form.instance.story = story
    #             form.save()
    #             return HttpResponseRedirect(reverse('news:story', kwargs={'pk': story_pk}))
    #     return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        pk = self.kwargs.get("pk")
        story = get_object_or_404(NewsStory, pk=pk)
        form.instance.story = story
        return super().form_valid(form)

    def get_queryset(self):
        return Comment.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.order_by('-pub_date')
        return context

    def get_success_url(self) -> str:
        pk = self.kwargs.get("pk")
        return reverse_lazy("news:story", kwargs={'pk':pk})


