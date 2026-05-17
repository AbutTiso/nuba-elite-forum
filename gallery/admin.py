from django.contrib import admin
from .models import GalleryCategory, GalleryItem

@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'media_type', 'is_featured', 'created_at']
    list_filter = ['category', 'media_type', 'is_featured', 'created_at']
    search_fields = ['title', 'caption', 'event_name']
    readonly_fields = ['created_at']
    fieldsets = (
        ('Media Details', {
            'fields': ('title', 'category', 'media_type', 'image', 'video_url')
        }),
        ('Information', {
            'fields': ('caption', 'event_name', 'event_date')
        }),
        ('Settings', {
            'fields': ('is_featured', 'created_at')
        }),
    )
    actions = ['mark_featured', 'unmark_featured']
    
    def mark_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} item(s) marked as featured.')
    mark_featured.short_description = 'Mark as featured'
    
    def unmark_featured(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} item(s) unmarked.')
    unmark_featured.short_description = 'Remove featured status'
