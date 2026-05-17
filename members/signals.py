from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Member
from core.email_notifications import send_welcome_email

@receiver(post_save, sender=User)
def create_member_profile(sender, instance, created, **kwargs):
    if created:
        Member.objects.get_or_create(
            user=instance,
            defaults={
                'full_name': instance.get_full_name() or instance.username,
                'email': instance.email,
                'country': 'Sudan',
                'is_approved': True,
            }
        )
        # Send welcome email
        send_welcome_email(instance)