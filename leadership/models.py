from django.db import models

class LeadershipMember(models.Model):
    ROLE_CHOICES = (
        ('chairperson', 'Chairperson'),
        ('vice_chair', 'Vice Chairperson'),
        ('secretary', 'Secretary General'),
        ('treasurer', 'Treasurer'),
        ('coordinator', 'Program Coordinator'),
        ('advisor', 'Advisor'),
        ('board', 'Board Member'),
    )
    
    full_name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    bio = models.TextField()
    expertise = models.CharField(max_length=300)
    email = models.EmailField(blank=True)
    linkedin = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    profile_image = models.ImageField(upload_to='leadership/')
    order = models.IntegerField(default=0, help_text='Display order (lower numbers first)')
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order', 'full_name']
        verbose_name = "Leadership Member"
        verbose_name_plural = "Leadership Members"
    
    def __str__(self):
        return f"{self.full_name} - {self.get_role_display()}"