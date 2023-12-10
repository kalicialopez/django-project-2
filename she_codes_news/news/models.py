from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

USER = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class NewsStory(models.Model):
    title = models.CharField(max_length=200)
    tagline = models.CharField(max_length=200)
    category = models.CharField(max_length=200, default='Uncategorised') 
    author = models.ForeignKey(
        USER, 
        on_delete=models.CASCADE
        )
    pub_date = models.DateTimeField()
    image = models.URLField(null=True, blank=True)
    content = models.TextField()
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news:story', kwargs={'pk': self.pk})

class Comment(models.Model):
    story = models.ForeignKey(NewsStory, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(USER, related_name='comments', on_delete=models.CASCADE, null=True)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    mod_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s | %s' % (self.story.title, self.commenter.username)
    
    def get_absolute_url(self):
        return reverse('news:comment', args=[str(self.id)])