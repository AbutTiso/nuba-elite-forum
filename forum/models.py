from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from tinymce.models import HTMLField

class ForumCategory(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    icon = models.CharField(max_length=10, default='💬')
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Forum Categories'
        ordering = ['order']
    
    def __str__(self):
        return self.name
    
    def thread_count(self):
        return self.threads.count()
    
    def latest_thread(self):
        return self.threads.order_by('-created_at').first()

class Thread(models.Model):
    category = models.ForeignKey(ForumCategory, on_delete=models.CASCADE, related_name='threads')
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, max_length=350)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forum_threads')
    content = HTMLField()
    tags = models.CharField(max_length=300, blank=True, help_text='Comma-separated tags')
    is_pinned = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_pinned', '-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def reply_count(self):
        return self.posts.count() - 1 if self.posts.count() > 0 else 0
    
    def last_reply(self):
        return self.posts.order_by('-created_at').first()

class Post(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forum_posts')
    content = HTMLField()
    is_edited = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f'Reply by {self.author.username} on {self.thread.title}'

class ThreadLike(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['thread', 'user']
    
    def __str__(self):
        return f'{self.user.username} liked {self.thread.title}'

class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['post', 'user']
    
    def __str__(self):
        return f'{self.user.username} liked a reply'