from django.shortcuts import render, redirect
from django.conf import settings
from django.utils import translation, timezone
from articles.models import Article
from events.models import Event
from forum.models import Thread
from members.models import Member

def home(request):
    lang = request.GET.get('lang')
    if lang and lang in dict(settings.LANGUAGES):
        response = redirect('core:home')
        response.set_cookie('site_lang', lang, max_age=365*24*60*60)
        return response
    
    site_lang = request.COOKIES.get('site_lang')
    if site_lang and site_lang in dict(settings.LANGUAGES):
        translation.activate(site_lang)
    
    latest_articles = Article.objects.filter(status='published').order_by('-published_at')[:3]
    upcoming_events = Event.objects.filter(event_date__gt=timezone.now()).order_by('event_date')[:2]
    
    context = {
        'page_title': 'Nuba Elite Forum (NEF) - Uniting Voices, Empowering Communities',
        'latest_articles': latest_articles,
        'upcoming_events': upcoming_events,
        'total_members': Member.objects.filter(is_approved=True).count(),
        'total_threads': Thread.objects.count(),
        'upcoming_events_count': Event.objects.filter(event_date__gt=timezone.now()).count(),
    }
    return render(request, 'core/home.html', context)

def about(request):
    context = {'page_title': 'About NEF'}
    return render(request, 'core/about.html', context)

def focus_areas(request):
    context = {'page_title': 'Focus Areas'}
    return render(request, 'core/focus_areas.html', context)
def donate(request):
    context = {'page_title': 'Support NEF'}
    return render(request, 'core/donate.html', context)