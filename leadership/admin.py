from django.contrib import admin
from django.utils.html import format_html
from .models import LeadershipMember

@admin.register(LeadershipMember)
class LeadershipMemberAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'role', 'order', 'is_active']
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
    
    def activate(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} leader(s) activated.')
    activate.short_description = 'Activate selected'
    
    def deactivate(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} leader(s) deactivated.')
    deactivate.short_description = 'Deactivate selected'
