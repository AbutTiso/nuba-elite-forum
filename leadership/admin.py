from django.contrib import admin
from django.utils.html import format_html
from .models import LeadershipMember

@admin.register(LeadershipMember)
class LeadershipMemberAdmin(admin.ModelAdmin):
    list_display = ['profile_preview', 'full_name', 'role', 'order', 'is_active_badge']
    list_filter = ['role', 'is_active']
    search_fields = ['full_name', 'expertise', 'bio']
    ordering = ['order']
    fieldsets = (
        ('Personal', {
            'fields': ('full_name', 'title', 'role', 'profile_image', 'order')
        }),
        ('Details', {
            'fields': ('bio', 'expertise')
        }),
        ('Contact', {
            'fields': ('email', 'linkedin', 'twitter')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    actions = ['activate', 'deactivate']
    
    def profile_preview(self, obj):
        if obj.profile_image:
            return format_html(
                '<img src="{}" style="width:40px;height:40px;border-radius:50%;object-fit:cover;border:2px solid #C8A24C;">',
                obj.profile_image.url
            )
        return format_html(
            '<div style="width:40px;height:40px;border-radius:50%;background:#062B57;color:#C8A24C;display:flex;align-items:center;justify-content:center;font-weight:bold;">{}</div>',
            obj.full_name[0]
        )
    profile_preview.short_description = 'Photo'
    
    def is_active_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="color:#00A651;">&#10003; Active</span>')
        return format_html('<span style="color:#D72638;">&#10007; Inactive</span>')
    is_active_badge.short_description = 'Status'
    
    def activate(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} leader(s) activated.')
    activate.short_description = 'Activate selected'
    
    def deactivate(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} leader(s) deactivated.')
    deactivate.short_description = 'Deactivate selected'
