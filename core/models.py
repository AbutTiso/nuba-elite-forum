from django.db import models

class SiteSetting(models.Model):
    site_name = models.CharField(max_length=100, default='Nuba Elite Forum')
    tagline = models.CharField(max_length=300, default='Uniting Voices. Empowering Communities.')
    about_text = models.TextField()
    mission_statement = models.TextField()
    vision_statement = models.TextField()
    contact_email = models.EmailField(default='info@nubaforum.org')
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Site Setting"
        verbose_name_plural = "Site Settings"
    
    def __str__(self):
        return self.site_name
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and SiteSetting.objects.exists():
            return
        super().save(*args, **kwargs)