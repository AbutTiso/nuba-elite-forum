from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ForumCategory, Thread, Post
from core.models import Notification

def forum_home(request):
    categories = ForumCategory.objects.all()
    recent_threads = Thread.objects.all().order_by('-created_at')[:10]
    
    context = {
        'categories': categories,
        'recent_threads': recent_threads,
        'page_title': 'Discussion Forums',
    }
    return render(request, 'forum/home.html', context)

def category_detail(request, slug):
    category = get_object_or_404(ForumCategory, slug=slug)
    threads = category.threads.all()
    
    context = {
        'category': category,
        'threads': threads,
        'page_title': category.name,
    }
    return render(request, 'forum/category.html', context)

def thread_detail(request, slug):
    thread = get_object_or_404(Thread, slug=slug)
    thread.views += 1
    thread.save()
    posts = thread.posts.all()
    
    if request.method == 'POST' and request.user.is_authenticated:
        if thread.is_closed:
            messages.error(request, 'This thread is closed.')
            return redirect('forum:thread', slug=slug)
        content = request.POST.get('content', '').strip()
        if content:
            Post.objects.create(thread=thread, author=request.user, content=content)
            # Notify thread author
            if thread.author != request.user:
                Notification.objects.create(
                    user=thread.author,
                    notification_type='thread_reply',
                    message=f'{request.user.username} replied to your thread \"{thread.title}\"',
                    link=f'/forum/thread/{thread.slug}/'
                )
            messages.success(request, 'Reply posted successfully!')
            return redirect('forum:thread', slug=slug)
    
    context = {
        'thread': thread,
        'posts': posts,
        'page_title': thread.title,
    }
    return render(request, 'forum/thread.html', context)

@login_required
def create_thread(request, slug):
    category = get_object_or_404(ForumCategory, slug=slug)
    
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        if title and content:
            thread = Thread.objects.create(
                category=category, title=title,
                author=request.user, content=content
            )
            Post.objects.create(thread=thread, author=request.user, content=content)
            messages.success(request, 'Thread created!')
            return redirect('forum:thread', slug=thread.slug)
    
    context = {
        'category': category,
        'page_title': f'New Thread — {category.name}',
    }
    return render(request, 'forum/create_thread.html', context)

@login_required
def reply_thread(request, slug):
    thread = get_object_or_404(Thread, slug=slug)
    if thread.is_closed:
        messages.error(request, 'Thread is closed.')
        return redirect('forum:thread', slug=slug)
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Post.objects.create(thread=thread, author=request.user, content=content)
            if thread.author != request.user:
                Notification.objects.create(
                    user=thread.author,
                    notification_type='thread_reply',
                    message=f'{request.user.username} replied to your thread \"{thread.title}\"',
                    link=f'/forum/thread/{thread.slug}/'
                )
            messages.success(request, 'Reply posted!')
    return redirect('forum:thread', slug=slug)

from .models import ThreadLike, PostLike
from django.http import JsonResponse

@login_required
def like_thread(request, slug):
    thread = get_object_or_404(Thread, slug=slug)
    like, created = ThreadLike.objects.get_or_create(thread=thread, user=request.user)
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    return JsonResponse({'liked': liked, 'count': thread.likes.count()})

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = PostLike.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    return JsonResponse({'liked': liked, 'count': post.likes.count()})