from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Count
from django.db.models.functions import TruncMonth
import json, datetime
from members.models import Member
from articles.models import Article, Category
from events.models import Event
from contact.models import ContactMessage, NewsletterSubscriber
from forum.models import Thread, Post

@staff_member_required
def dashboard(request):
    six_months_ago = timezone.now() - datetime.timedelta(days=180)
    monthly_data = Member.objects.filter(application_date__gte=six_months_ago).annotate(month=TruncMonth('application_date')).values('month').annotate(count=Count('id')).order_by('month')
    
    context = {
        'total_members': Member.objects.filter(is_approved=True).count(),
        'pending_members': Member.objects.filter(is_approved=False).count(),
        'published_articles': Article.objects.filter(status='published').count(),
        'upcoming_events': Event.objects.filter(event_date__gt=timezone.now()).count(),
        'unread_messages': ContactMessage.objects.filter(is_read=False).count(),
        'total_threads': Thread.objects.count(),
        'total_posts': Post.objects.count(),
        'recent_members': Member.objects.all().order_by('-application_date')[:5],
        'recent_messages': ContactMessage.objects.all().order_by('-created_at')[:5],
        'monthly_labels': json.dumps([d['month'].strftime('%Y-%m') for d in monthly_data]),
        'monthly_counts_json': json.dumps([d['count'] for d in monthly_data]),
    }
    return render(request, 'custom_admin/dashboard.html', context)

@staff_member_required
def members(request):
    status_filter = request.GET.get('status', '')
    members_list = Member.objects.all().order_by('-application_date')
    if status_filter == 'pending': members_list = members_list.filter(is_approved=False)
    elif status_filter == 'approved': members_list = members_list.filter(is_approved=True, user__is_staff=False)
    elif status_filter == 'admin': members_list = members_list.filter(user__is_staff=True)
    return render(request, 'custom_admin/members.html', {'members': members_list, 'current_filter': status_filter})

@staff_member_required
def approve_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    member.is_approved = True; member.save()
    messages.success(request, f'{member.full_name} approved.')
    return redirect('custom_admin:members')

@staff_member_required
def suspend_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    member.is_approved = False; member.save()
    messages.success(request, f'{member.full_name} suspended.')
    return redirect('custom_admin:members')

@staff_member_required
def delete_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    if member.user and member.user == request.user:
        messages.error(request, 'Cannot delete yourself.')
        return redirect('custom_admin:members')
    name = member.full_name
    if member.user: member.user.delete()
    else: member.delete()
    messages.success(request, f'{name} deleted.')
    return redirect('custom_admin:members')

@staff_member_required
def make_admin(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    if member.user:
        member.user.is_staff = True; member.user.save()
        messages.success(request, f'{member.full_name} is now admin.')
    return redirect('custom_admin:members')

@staff_member_required
def remove_admin(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    if member.user and member.user == request.user:
        messages.error(request, 'Cannot remove your own admin.')
        return redirect('custom_admin:members')
    if member.user:
        member.user.is_staff = False; member.user.save()
        messages.success(request, f'Admin removed from {member.full_name}.')
    return redirect('custom_admin:members')

@staff_member_required
def articles(request):
    return render(request, 'custom_admin/articles.html', {'articles': Article.objects.all().order_by('-created_at')})

@staff_member_required
def create_article(request):
    if request.method == 'POST':
        slug = request.POST.get('slug') or request.POST['title'].lower().replace(' ', '-')
        Article.objects.create(title=request.POST['title'], slug=slug, content=request.POST['content'], excerpt=request.POST.get('excerpt', ''), author=request.POST.get('author', 'NEF Editorial'), status=request.POST.get('status', 'published'), category_id=request.POST.get('category'), published_at=timezone.now() if request.POST.get('status') == 'published' else None)
        messages.success(request, 'Article created!')
        return redirect('custom_admin:articles')
    return render(request, 'custom_admin/create_article.html', {'categories': Category.objects.all()})

@staff_member_required
def edit_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.method == 'POST':
        article.title = request.POST['title']; article.content = request.POST['content']
        article.excerpt = request.POST.get('excerpt', ''); article.status = request.POST.get('status', 'published')
        if request.POST.get('status') == 'published' and not article.published_at: article.published_at = timezone.now()
        article.save()
        messages.success(request, 'Article updated!')
        return redirect('custom_admin:articles')
    return render(request, 'custom_admin/edit_article.html', {'article': article})

@staff_member_required
def delete_article(request, article_id):
    get_object_or_404(Article, id=article_id).delete()
    messages.success(request, 'Article deleted.')
    return redirect('custom_admin:articles')

@staff_member_required
def events(request):
    return render(request, 'custom_admin/events.html', {'events': Event.objects.all().order_by('-event_date')})

@staff_member_required
def create_event(request):
    if request.method == 'POST':
        slug = request.POST.get('slug') or request.POST['title'].lower().replace(' ', '-')
        Event.objects.create(title=request.POST['title'], slug=slug, description=request.POST['description'], short_description=request.POST.get('short_description', ''), event_type=request.POST.get('event_type', 'forum'), event_date=request.POST['event_date'], venue=request.POST.get('venue', ''))
        messages.success(request, 'Event created!')
        return redirect('custom_admin:events')
    return render(request, 'custom_admin/create_event.html')

@staff_member_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.title = request.POST['title']; event.description = request.POST['description']
        event.short_description = request.POST.get('short_description', '')
        event.event_type = request.POST.get('event_type', event.event_type)
        event.event_date = request.POST['event_date']; event.venue = request.POST.get('venue', '')
        event.save()
        messages.success(request, 'Event updated!')
        return redirect('custom_admin:events')
    return render(request, 'custom_admin/edit_event.html', {'event': event})

@staff_member_required
def delete_event(request, event_id):
    get_object_or_404(Event, id=event_id).delete()
    messages.success(request, 'Event deleted.')
    return redirect('custom_admin:events')

@staff_member_required
def messages_view(request):
    return render(request, 'custom_admin/messages.html', {'messages': ContactMessage.objects.all().order_by('-created_at')})

@staff_member_required
def subscribers(request):
    return render(request, 'custom_admin/subscribers.html', {'subscribers': NewsletterSubscriber.objects.all().order_by('-subscribed_at')})
