from django import forms
from .models import Member

class MemberApplicationForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = [
            'full_name', 'email', 'phone', 'profession', 
            'organization', 'country', 'city', 'membership_type',
            'interest_areas', 'bio', 'motivation', 'profile_image'
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
            'motivation': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell us why you want to join NEF and how you can contribute...'}),
            'interest_areas': forms.TextInput(attrs={'placeholder': 'e.g., Education, Peacebuilding, Youth'}),
            'full_name': forms.TextInput(attrs={'placeholder': 'Your full name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'your@email.com'}),
            'phone': forms.TextInput(attrs={'placeholder': '+249...'}),
            'profession': forms.TextInput(attrs={'placeholder': 'e.g., Teacher, Engineer, Student'}),
            'organization': forms.TextInput(attrs={'placeholder': 'Your organization or university'}),
            'country': forms.TextInput(attrs={'placeholder': 'Your country'}),
            'city': forms.TextInput(attrs={'placeholder': 'Your city'}),
        }
        labels = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone': 'Phone Number',
            'profession': 'Profession / Occupation',
            'organization': 'Organization / Institution',
            'country': 'Country',
            'city': 'City',
            'membership_type': 'Membership Type',
            'interest_areas': 'Areas of Interest',
            'bio': 'Short Bio',
            'motivation': 'Why do you want to join NEF?',
            'profile_image': 'Profile Photo (optional)',
        }
