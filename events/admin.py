from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_type', 'event_date', 'status_badge', 'is_featured', 'created_at']
    list_filter = ['event_type', 'is_featured', 'is_virtual', 'event_date']
    search_fields = ['title', 'description', 'venue']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'event_date'
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Event Details', {
            'fields': ('title', 'slug', 'event_type', 'description', 'short_description')
        }),
        ('Date & Location', {
            'fields': ('event_date', 'end_date', 'venue', 'is_virtual', 'registration_link')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Settings', {
            'fields': ('is_featured',)
        }),
    )
    actions = ['mark_featured', 'unmark_featured']
    
    def status_badge(self, obj):
        if obj.event_date > timezone.now():
            return format_html(
                '<span style="background:#00A651;color:white;padding:3px 10px;border-radius:12px;font-size:11px;font-weight:600;">Upcoming</span>'
            )
        return format_html(
            '<span style="background:#6B7280;color:white;padding:3px 10px;border-radius:12px;font-size:11px;font-weight:600;">Past</span>'
        )
    status_badge.short_description = 'Status'
    
    def mark_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} event(s) marked as featured.')
    mark_featured.short_description = 'Mark as featured'
    
    def unmark_featured(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} event(s) unmarked.')
    unmark_featured.short_description = 'Remove featured status'
