from django.core.mail import send_mail
from django.conf import settings

def send_thread_reply_notification(thread, reply_author):
    if thread.author.email:
        subject = f'New reply to your thread: {thread.title}'
        message = f'''Hi {thread.author.username},

{reply_author.username} replied to your thread "{thread.title}" on Nuba Elite Forum.

View it here: http://127.0.0.1:8000/forum/thread/{thread.slug}/

— Nuba Elite Forum'''
        
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL or 'noreply@nubaforum.org', [thread.author.email])

def send_welcome_email(user):
    if user.email:
        subject = 'Welcome to Nuba Elite Forum!'
        message = f'''Hi {user.username},

Welcome to the Nuba Elite Forum community! You can now participate in discussions, connect with fellow members, and contribute to building a better Sudan.

Get started: http://127.0.0.1:8000/forum/

— Nuba Elite Forum'''
        
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL or 'noreply@nubaforum.org', [user.email])

def send_message_notification(recipient, sender):
    if recipient.email:
        subject = f'New message from {sender.username}'
        message = f'''Hi {recipient.username},

You have a new message from {sender.username} on Nuba Elite Forum.

View it here: http://127.0.0.1:8000/messages/

— Nuba Elite Forum'''
        
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL or 'noreply@nubaforum.org', [recipient.email])
