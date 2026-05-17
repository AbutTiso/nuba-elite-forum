from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    verbose_name = 'NEF Core'

    def ready(self):
        # Import and patch admin after all models are loaded
        from django.contrib import admin
        from django.utils import timezone
        from members.models import Member
        from articles.models import Article
        from events.models import Event
        from contact.models import ContactMessage

        original_index = admin.site.index

        def dashboard_index(request, extra_context=None):
            if extra_context is None:
                extra_context = {}
            extra_context['total_members'] = Member.objects.count()
            extra_context['pending_members'] = Member.objects.filter(is_approved=False).count()
            extra_context['published_articles'] = Article.objects.filter(status='published').count()
            extra_context['upcoming_events_count'] = Event.objects.filter(event_date__gt=timezone.now()).count()
            extra_context['unread_messages'] = ContactMessage.objects.filter(is_read=False).count()
            extra_context['recent_members'] = Member.objects.all().order_by('-application_date')[:5]
            extra_context['recent_messages'] = ContactMessage.objects.all().order_by('-created_at')[:5]
            return original_index(request, extra_context)

        admin.site.index = dashboard_index
