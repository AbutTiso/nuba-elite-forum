from django.shortcuts import render
from django.db.models import Q
from articles.models import Article
from forum.models import Thread, Post
from events.models import Event

def search(request):
    query = request.GET.get('q', '').strip()
    results = {'articles': [], 'threads': [], 'events': []}
    
    if query:
        results['articles'] = Article.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query),
            status='published'
        )[:10]
        results['threads'] = Thread.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )[:10]
        results['events'] = Event.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )[:5]
    
    total = len(results['articles']) + len(results['threads']) + len(results['events'])
    
    context = {
        'query': query,
        'results': results,
        'total': total,
        'page_title': f'Search: {query}' if query else 'Search',
    }
    return render(request, 'core/search.html', context)
