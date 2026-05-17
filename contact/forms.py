from django import forms
from .models import ContactMessage, NewsletterSubscriber

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message', 'organization']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your full name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'your@email.com'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Message subject'}),
            'organization': forms.TextInput(attrs={'placeholder': 'Your organization (optional)'}),
            'message': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Your message...'}),
        }

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ['email', 'name']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'your@email.com'}),
            'name': forms.TextInput(attrs={'placeholder': 'Your name (optional)'}),
        }
