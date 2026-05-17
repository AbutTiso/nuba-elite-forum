from django.contrib import admin
from .models import ForumCategory, Thread, Post

class PostInline(admin.TabularInline):
    model = Post
    extra = 0
    readonly_fields = ['created_at']

@admin.register(ForumCategory)
class ForumCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'thread_count', 'order']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order']

@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'views', 'reply_count', 'is_pinned', 'is_closed', 'created_at']
    list_filter = ['category', 'is_pinned', 'is_closed', 'created_at']
    search_fields = ['title', 'content', 'author__username']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [PostInline]
    actions = ['pin_threads', 'unpin_threads', 'close_threads', 'open_threads']
    
    def pin_threads(self, request, queryset):
        queryset.update(is_pinned=True)
        self.message_user(request, 'Threads pinned.')
    pin_threads.short_description = 'Pin threads'
    
    def unpin_threads(self, request, queryset):
        queryset.update(is_pinned=False)
        self.message_user(request, 'Threads unpinned.')
    unpin_threads.short_description = 'Unpin threads'
    
    def close_threads(self, request, queryset):
        queryset.update(is_closed=True)
        self.message_user(request, 'Threads closed.')
    close_threads.short_description = 'Close threads'
    
    def open_threads(self, request, queryset):
        queryset.update(is_closed=False)
        self.message_user(request, 'Threads opened.')
    open_threads.short_description = 'Open threads'

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['thread', 'author', 'created_at', 'is_edited']
    list_filter = ['created_at', 'is_edited']
    search_fields = ['content', 'author__username']
