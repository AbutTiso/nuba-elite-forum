from django.contrib import admin
from django.utils import timezone
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_type', 'event_date', 'is_featured', 'created_at']
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
    
    def mark_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} event(s) marked as featured.')
    mark_featured.short_description = 'Mark as featured'
    
    def unmark_featured(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} event(s) unmarked.')
    unmark_featured.short_description = 'Remove featured status'
