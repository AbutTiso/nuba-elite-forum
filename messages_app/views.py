from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from .models import Conversation, Message
from django.contrib.auth.models import User

@login_required
def inbox(request):
    conversations = Conversation.objects.filter(participants=request.user)
    unread_total = sum(c.unread_count(request.user) for c in conversations)
    
    context = {
        'conversations': conversations,
        'unread_total': unread_total,
        'page_title': 'Messages',
    }
    return render(request, 'messages_app/inbox.html', context)

@login_required
def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
    
    # Mark messages as read
    conversation.messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)
    
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Message.objects.create(conversation=conversation, sender=request.user, content=content)
            conversation.save()  # Update timestamp
            return redirect('messages:conversation', conversation_id=conversation.id)
    
    context = {
        'conversation': conversation,
        'page_title': 'Conversation',
    }
    return render(request, 'messages_app/conversation.html', context)

@login_required
def start_conversation(request, username):
    other_user = get_object_or_404(User, username=username)
    
    if other_user == request.user:
        messages.error(request, 'You cannot message yourself.')
        return redirect('messages:inbox')
    
    # Check if conversation already exists
    existing = Conversation.objects.filter(
        participants=request.user
    ).filter(
        participants=other_user
    ).first()
    
    if existing:
        return redirect('messages:conversation', conversation_id=existing.id)
    
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            conversation = Conversation.objects.create()
            conversation.participants.add(request.user, other_user)
            Message.objects.create(conversation=conversation, sender=request.user, content=content)
            messages.success(request, 'Message sent!')
            return redirect('messages:conversation', conversation_id=conversation.id)
    
    context = {
        'other_user': other_user,
        'page_title': f'Message {other_user.username}',
    }
    return render(request, 'messages_app/start.html', context)

@login_required
def unread_count(request):
    count = sum(
        c.unread_count(request.user) 
        for c in Conversation.objects.filter(participants=request.user)
    )
    return JsonResponse({'unread': count})
