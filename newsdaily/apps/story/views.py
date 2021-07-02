from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import StoryForm, CommentForm
from .models import Story, Vote, Comment
# Create your views here.


import datetime


def main(request):
    from_date = datetime.datetime.now() - datetime.timedelta(days=1)
    stories = Story.objects.filter(created_at__gte=from_date).order_by('-number_of_votes')[:10]

    return render(request, 'story/main.html', {'stories':stories})

def latest(request):
    stories = Story.objects.all()[:200]
    return render(request, 'story/latest.html', {'stories':stories})

@login_required
def vote(request, story_id):
    story = get_object_or_404(Story, pk=story_id)

    next_page = request.GET.get('next_page', '')
    if story.created_by != request.user and not Vote.objects.filter(created_by=request.user, Story=story):
        vote = Vote.objects.create(Story=story, created_by = request.user)
    

    if next_page == 'story':
        return redirect('story', story_id=story_id)
    
    else:
        return redirect('main')

def story(request, story_id):
    story = get_object_or_404(Story, pk=story_id)
    form_class = CommentForm
    form = form_class(request.POST)
    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.Story = story
            comment.created_by = request.user
            comment.save()

            return redirect('story', story_id = story_id)
        
        else:
            form = CommentForm()

    return render(request, 'story/detail.html', {'story':story, 'form':form})

@login_required
def write_story(request):
    if request.method == 'POST':
        form = StoryForm(request.POST)

        if form.is_valid():
            story = form.save(commit=False)#we need to pass other fields
            story.created_by = request.user
            story.save()
            return redirect('main')
    else:
        form = StoryForm()

    return render(request, 'story/submit.html',{'form':form})


def search(request):
    query = request.GET.get('query', '')
    if len(query)>0:
        stories = Story.objects.filter(title__icontains=query)
    
    else:
        stories = []

    return render(request, 'story/search.html', {'stories':stories, 'query':query})