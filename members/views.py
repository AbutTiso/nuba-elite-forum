from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import MemberApplicationForm

def join(request):
    if request.method == 'POST':
        form = MemberApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            member = form.save()
            messages.success(request, 'Your application has been submitted successfully! We will review it and get back to you soon.')
            return redirect('members:join_success')
    else:
        form = MemberApplicationForm()
    
    context = {
        'form': form,
        'page_title': 'Join NEF',
    }
    return render(request, 'members/join.html', context)

def join_success(request):
    context = {
        'page_title': 'Application Submitted',
    }
    return render(request, 'members/join_success.html', context)
