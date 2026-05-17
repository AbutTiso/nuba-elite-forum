from django.shortcuts import render
from .models import Event

def event_list(request):
    events = Event.objects.all().order_by('-event_date')
    upcoming = [e for e in events if e.is_upcoming]
    past = [e for e in events if not e.is_upcoming]
    
    context = {
        'upcoming_events': upcoming,
        'past_events': past,
        'page_title': 'Events',
    }
    return render(request, 'events/list.html', context)
