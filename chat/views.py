from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import get_user_model
from .models import Thread, Message

User = get_user_model()

@login_required
def inbox(request):
    threads = request.user.threads.all().order_by('-updated_at')
    context = {
        'threads': threads,
    }
    return render(request, 'chat/inbox.html', context)

@login_required
def thread_detail(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    
    if request.user not in thread.participants.all():
        return redirect('inbox')
        
    unread_messages = thread.messages.exclude(sender=request.user).filter(is_read=False)
    unread_messages.update(is_read=True)
        
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(
                thread=thread,
                sender=request.user,
                content=content
            )
            # thread.updated_at is handled by auto_now=True in model
            thread.save()
            return redirect('thread_detail', thread_id=thread_id)
            
    other_user = thread.participants.exclude(id=request.user.id).first()
            
    context = {
        'thread': thread,
        'messages': thread.get_messages(),
        'other_user': other_user
    }
    return render(request, 'chat/room.html', context)

@login_required
def start_chat(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    thread = Thread.get_or_create(request.user, other_user)
    return redirect('thread_detail', thread_id=thread.id)
