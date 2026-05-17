from django.db import models
from django.utils import timezone

class Event(models.Model):
    EVENT_TYPE = (
        ('conference', 'Conference'),
        ('webinar', 'Webinar'),
        ('workshop', 'Workshop'),
        ('forum', 'Forum'),
        ('meeting', 'Meeting'),
        ('youth_program', 'Youth Program'),
    )
    
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True, max_length=250)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE, default='forum')
    description = models.TextField()
    short_description = models.TextField(max_length=300)
    venue = models.CharField(max_length=250, blank=True)
    event_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    registration_link = models.URLField(blank=True)
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    is_virtual = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-event_date']
    
    def __str__(self):
        return self.title
    
    @property
    def is_upcoming(self):
        return self.event_date > timezone.now()