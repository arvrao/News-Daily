from django import forms

from .models import Story, Comment

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ('title','url', 'story')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)