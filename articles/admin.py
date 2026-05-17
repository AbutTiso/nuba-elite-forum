from django.contrib import admin
from django.utils.html import format_html
from .models import Article, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'article_count']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    
    def article_count(self, obj):
        count = obj.articles.filter(status='published').count()
        return format_html('<strong>{}</strong>', count)
    article_count.short_description = 'Published Articles'

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'status_badge', 'featured_badge', 'published_at', 'created_at']
    list_filter = ['status', 'category', 'featured', 'created_at', 'published_at']
    search_fields = ['title', 'content', 'author', 'excerpt']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'category', 'author', 'content', 'excerpt')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Publishing', {
            'fields': ('status', 'featured', 'published_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    actions = ['publish_articles', 'unpublish_articles', 'mark_featured', 'unmark_featured']
    
    def status_badge(self, obj):
        if obj.status == 'published':
            return format_html(
                '<span style="background:#00A651;color:white;padding:3px 10px;border-radius:12px;font-size:11px;font-weight:600;">Published</span>'
            )
        return format_html(
            '<span style="background:#F59E0B;color:white;padding:3px 10px;border-radius:12px;font-size:11px;font-weight:600;">Draft</span>'
        )
    status_badge.short_description = 'Status'
    
    def featured_badge(self, obj):
        if obj.featured:
            return format_html(
                '<span style="color:#C8A24C;font-size:14px;">&#9733;</span>'
            )
        return '-'
    featured_badge.short_description = 'Featured'
    
    def publish_articles(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(status='published', published_at=timezone.now())
        self.message_user(request, f'{updated} article(s) published.')
    publish_articles.short_description = 'Publish selected articles'
    
    def unpublish_articles(self, request, queryset):
        updated = queryset.update(status='draft')
        self.message_user(request, f'{updated} article(s) unpublished.')
    unpublish_articles.short_description = 'Unpublish selected articles'
    
    def mark_featured(self, request, queryset):
        updated = queryset.update(featured=True)
        self.message_user(request, f'{updated} article(s) marked as featured.')
    mark_featured.short_description = 'Mark as featured'
    
    def unmark_featured(self, request, queryset):
        updated = queryset.update(featured=False)
        self.message_user(request, f'{updated} article(s) unmarked as featured.')
    unmark_featured.short_description = 'Remove featured status'
