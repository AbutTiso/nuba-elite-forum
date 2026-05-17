from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm, NewsletterForm

def contact_view(request):
    contact_form = ContactForm()
    newsletter_form = NewsletterForm()
    
    if request.method == 'POST':
        if 'contact_submit' in request.POST:
            contact_form = ContactForm(request.POST)
            if contact_form.is_valid():
                contact_form.save()
                messages.success(request, 'Your message has been sent successfully! We will get back to you soon.')
                return redirect('contact:contact')
        
        elif 'newsletter_submit' in request.POST:
            newsletter_form = NewsletterForm(request.POST)
            if newsletter_form.is_valid():
                newsletter_form.save()
                messages.success(request, 'You have been subscribed to our newsletter!')
                # Redirect back to the page they were on
                referer = request.META.get('HTTP_REFERER', '/')
                return redirect(referer)
    
    context = {
        'contact_form': contact_form,
        'newsletter_form': newsletter_form,
        'page_title': 'Contact Us',
    }
    return render(request, 'contact/contact.html', context)
