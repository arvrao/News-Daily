from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Story(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField()
    story = models.TextField(default='type here')
    number_of_votes = models.IntegerField(default=1)

    created_by = models.ForeignKey(User, related_name='stories',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return '%s' %self.title

class Vote(models.Model):
    Story = models.ForeignKey(Story, related_name='votes', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='votes',on_delete=models.CASCADE)
   # after creating each vote, increase num_votes by 1
    def save(self, *args, **kwargs):
        self.Story.number_of_votes = self.Story.number_of_votes+1 # .Story refers to attributes of Story class
        self.Story.save()
    
        super(Vote,self).save(*args, **kwargs)


class Comment(models.Model):
    Story = models.ForeignKey(Story, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField(default=None)

    created_by = models.ForeignKey(User, related_name='comments',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']