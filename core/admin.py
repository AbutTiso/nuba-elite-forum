from django.contrib import admin
from django.db.models import Count
from django.utils import timezone
import datetime
import json
from members.models import Member
from articles.models import Article
from events.models import Event
from contact.models import ContactMessage
from forum.models import Thread, Post
from .models import SiteSetting

@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

_original_index = admin.site.index
def _index_wrapper(request, extra_context=None):
    if extra_context is None:
        extra_context = {}
    extra_context['total_members'] = Member.objects.count()
    extra_context['pending_members'] = Member.objects.filter(is_approved=False).count()
    extra_context['published_articles'] = Article.objects.filter(status='published').count()
    extra_context['upcoming_events_count'] = Event.objects.filter(event_date__gt=timezone.now()).count()
    extra_context['unread_messages'] = ContactMessage.objects.filter(is_read=False).count()
    extra_context['recent_members'] = Member.objects.all().order_by('-application_date')[:5]
    extra_context['recent_messages'] = ContactMessage.objects.all().order_by('-created_at')[:5]
    extra_context['total_threads'] = Thread.objects.count()
    extra_context['total_posts'] = Post.objects.count()
    
    # Monthly member data for chart
    monthly_data = Member.objects.filter(
        application_date__gte=timezone.now() - datetime.timedelta(days=180)
    ).extra(
        select={'month': "strftime('%%Y-%%m', application_date)"}
    ).values('month').annotate(count=Count('id')).order_by('month')
    
    extra_context['monthly_labels'] = json.dumps([d['month'] for d in monthly_data])
    extra_context['monthly_counts_json'] = json.dumps([d['count'] for d in monthly_data])
    
    return _original_index(request, extra_context)

admin.site.index = _index_wrapper
