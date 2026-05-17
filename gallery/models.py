from django.db import models

class GalleryCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    
    class Meta:
        verbose_name_plural = 'Gallery Categories'
    
    def __str__(self):
        return self.name

class GalleryItem(models.Model):
    MEDIA_TYPE = (
        ('image', 'Image'),
        ('video', 'Video'),
    )
    
    title = models.CharField(max_length=200)
    category = models.ForeignKey(GalleryCategory, on_delete=models.CASCADE, related_name='items')
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE, default='image')
    image = models.ImageField(upload_to='gallery/', blank=True, null=True)
    video_url = models.URLField(blank=True, help_text='YouTube or Vimeo embed URL')
    caption = models.TextField(blank=True)
    event_name = models.CharField(max_length=200, blank=True)
    event_date = models.DateField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
