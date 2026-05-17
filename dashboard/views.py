from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from forum.models import Thread, Post
from articles.models import Article
from events.models import Event
from members.models import Member
from core.models import Notification

@login_required
def dashboard_home(request):
    my_threads = Thread.objects.filter(author=request.user).count()
    my_posts = Post.objects.filter(author=request.user).count()
    recent_threads = Thread.objects.all().order_by('-created_at')[:5]
    recent_posts = Post.objects.all().order_by('-created_at')[:5]
    latest_articles = Article.objects.filter(status='published').order_by('-published_at')[:3]
    upcoming_events = Event.objects.filter(event_date__gt=timezone.now()).order_by('event_date')[:3]
    unread_notifs = Notification.objects.filter(user=request.user, is_read=False).count()
    
    try:
        member = request.user.member_profile
    except:
        member = None
    
    total_members = Member.objects.filter(is_approved=True).count()
    total_threads = Thread.objects.count()
    total_posts = Post.objects.count()
    
    context = {
        'page_title': 'My Dashboard',
        'my_threads': my_threads,
        'my_posts': my_posts,
        'recent_threads': recent_threads,
        'recent_posts': recent_posts,
        'latest_articles': latest_articles,
        'upcoming_events': upcoming_events,
        'member': member,
        'total_members': total_members,
        'total_threads': total_threads,
        'total_posts': total_posts,
        'unread_notifs': unread_notifs,
    }
    return render(request, 'dashboard/home.html', context)

@login_required
def notifications(request):
    notifs = Notification.objects.filter(user=request.user).order_by('-created_at')[:20]
    unread = notifs.filter(is_read=False).count()
    
    if request.GET.get('mark_read'):
        notifs.filter(is_read=False).update(is_read=True)
        return JsonResponse({'status': 'ok'})
    
    data = [{
        'id': n.id, 'message': n.message, 'link': n.link,
        'is_read': n.is_read, 'created': n.created_at.strftime('%b %d, %Y'),
    } for n in notifs]
    return JsonResponse({'notifications': data, 'unread': unread})

@login_required
def profile(request):
    try:
        member = request.user.member_profile
    except:
        member = None
    
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()
        if member:
            member.full_name = request.POST.get('full_name', member.full_name)
            member.phone = request.POST.get('phone', member.phone)
            member.country = request.POST.get('country', member.country)
            member.city = request.POST.get('city', member.city)
            member.profession = request.POST.get('profession', member.profession)
            member.organization = request.POST.get('organization', member.organization)
            member.bio = request.POST.get('bio', member.bio)
            member.save()
        messages.success(request, 'Profile updated!')
        return redirect('dashboard:profile')
    
    context = {'page_title': 'My Profile', 'member': member}
    return render(request, 'dashboard/profile.html', context)

@login_required
def my_threads(request):
    my_threads = Thread.objects.filter(author=request.user).order_by('-created_at')
    all_threads = Thread.objects.all().order_by('-created_at')
    context = {
        'my_threads': my_threads,
        'all_threads': all_threads,
        'page_title': 'Threads'
    }
    return render(request, 'dashboard/my_threads.html', context)

@login_required
def my_posts(request):
    my_posts = Post.objects.filter(author=request.user).order_by('-created_at')
    all_posts = Post.objects.all().order_by('-created_at')
    context = {
        'my_posts': my_posts,
        'all_posts': all_posts,
        'page_title': 'Replies'
    }
    return render(request, 'dashboard/my_posts.html', context)
