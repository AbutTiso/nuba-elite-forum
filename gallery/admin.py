from django.contrib import admin
from django.utils.html import format_html
from .models import GalleryCategory, GalleryItem

@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'item_count']
    prepopulated_fields = {'slug': ('name',)}
    
    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = 'Items'

@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ['thumbnail', 'title', 'category', 'media_type', 'is_featured', 'created_at']
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
    
    def thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:50px;height:50px;border-radius:8px;object-fit:cover;">',
                obj.image.url
            )
        return format_html(
            '<div style="width:50px;height:50px;border-radius:8px;background:#062B57;color:#C8A24C;display:flex;align-items:center;justify-content:center;">{}</div>',
            '&#9654;' if obj.media_type == 'video' else '&#128247;'
        )
    thumbnail.short_description = 'Preview'
    
    def mark_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} item(s) marked as featured.')
    mark_featured.short_description = 'Mark as featured'
    
    def unmark_featured(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} item(s) unmarked.')
    unmark_featured.short_description = 'Remove featured status'
