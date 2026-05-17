from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Member

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'membership_type', 'country', 'status_badge', 'application_date']
    list_filter = ['membership_type', 'country', 'is_approved', 'application_date']
    search_fields = ['full_name', 'email', 'profession', 'organization', 'country', 'city']
    readonly_fields = ['application_date']
    fieldsets = (
        ('Personal Information', {
            'fields': ('full_name', 'email', 'phone', 'country', 'city')
        }),
        ('Professional Background', {
            'fields': ('profession', 'organization', 'membership_type', 'interest_areas')
        }),
        ('Application Details', {
            'fields': ('bio', 'motivation', 'profile_image')
        }),
        ('Status', {
            'fields': ('is_approved', 'application_date')
        }),
    )
    actions = ['approve_members', 'suspend_members', 'reject_members']
    
    def status_badge(self, obj):
        if obj.is_approved:
            return format_html(
                '<span style="background:#00A651;color:white;padding:4px 12px;border-radius:20px;font-size:12px;font-weight:600;">Approved</span>'
            )
        return format_html(
            '<span style="background:#D72638;color:white;padding:4px 12px;border-radius:20px;font-size:12px;font-weight:600;">Pending</span>'
        )
    status_badge.short_description = 'Status'
    
    def approve_members(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} member(s) approved successfully.')
    approve_members.short_description = 'Approve selected members'
    
    def suspend_members(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'{updated} member(s) suspended.')
    suspend_members.short_description = 'Suspend selected members'
    
    def reject_members(self, request, queryset):
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f'{count} member(s) rejected and removed.')
    reject_members.short_description = 'Reject and delete selected members'
