from django.db import models
from django.contrib.auth.models import User

class Member(models.Model):
    MEMBERSHIP_TYPE = (
        ('individual', 'Individual'),
        ('student', 'Student'),
        ('professional', 'Professional'),
        ('organization', 'Organization'),
    )
    
    INTEREST_CHOICES = (
        ('education', 'Education & Leadership'),
        ('peacebuilding', 'Peacebuilding & Governance'),
        ('youth', 'Youth Empowerment'),
        ('economy', 'Economic Development'),
        ('culture', 'Culture & Identity'),
        ('health', 'Public Health'),
        ('innovation', 'Innovation & Technology'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='member_profile')
    full_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50, blank=True)
    profession = models.CharField(max_length=200, blank=True)
    organization = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100, blank=True)
    membership_type = models.CharField(max_length=20, choices=MEMBERSHIP_TYPE, default='individual')
    interest_areas = models.CharField(max_length=500, help_text='Comma-separated interests')
    bio = models.TextField(blank=True)
    motivation = models.TextField(help_text='Why do you want to join NEF?', blank=True)
    profile_image = models.ImageField(upload_to='members/', blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    application_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-application_date']
    
    def __str__(self):
        return self.full_name
