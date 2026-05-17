from django.shortcuts import render
from .models import LeadershipMember

def leadership_list(request):
    members = LeadershipMember.objects.filter(is_active=True).order_by('order')
    
    context = {
        'members': members,
        'page_title': 'Leadership',
    }
    return render(request, 'leadership/list.html', context)
