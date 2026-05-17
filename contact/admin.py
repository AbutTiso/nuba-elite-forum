from django.contrib import admin
from django.utils.html import format_html
from .models import ContactMessage, NewsletterSubscriber

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read_badge', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['created_at']
    fieldsets = (
        ('Sender', {
            'fields': ('name', 'email', 'organization')
        }),
        ('Message', {
            'fields': ('subject', 'message')
        }),
        ('Status', {
            'fields': ('is_read', 'created_at')
        }),
    )
    actions = ['mark_read', 'mark_unread']
    
    def is_read_badge(self, obj):
        if obj.is_read:
            return format_html(
                '<span style="color:#00A651;">&#10003; Read</span>'
            )
        return format_html(
            '<span style="color:#D72638;font-weight:600;">&#9679; Unread</span>'
        )
    is_read_badge.short_description = 'Status'
    
    def mark_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} message(s) marked as read.')
    mark_read.short_description = 'Mark as read'
    
    def mark_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} message(s) marked as unread.')
    mark_unread.short_description = 'Mark as unread'

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'is_active_badge', 'subscribed_at']
    list_filter = ['is_active', 'subscribed_at']
    search_fields = ['email', 'name']
    actions = ['activate', 'deactivate']
    
    def is_active_badge(self, obj):
        if obj.is_active:
            return format_html(
                '<span style="background:#00A651;color:white;padding:3px 10px;border-radius:12px;font-size:11px;">Active</span>'
            )
        return format_html(
            '<span style="background:#D72638;color:white;padding:3px 10px;border-radius:12px;font-size:11px;">Inactive</span>'
        )
    is_active_badge.short_description = 'Status'
    
    def activate(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} subscriber(s) activated.')
    activate.short_description = 'Activate selected subscribers'
    
    def deactivate(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} subscriber(s) deactivated.')
    deactivate.short_description = 'Deactivate selected subscribers'
