from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Message
from .forms import MessageForm
from django.contrib.auth.models import User

@login_required
def chat_room(request, receiver_id):
    # Fetch the receiver user or return a 404 if not found
    receiver = get_object_or_404(User, id=receiver_id)

    # Fetch messages between the current user and the receiver
    messages = Message.objects.filter(
        sender=request.user, receiver=receiver
    ) | Message.objects.filter(
        sender=receiver, receiver=request.user
    ).order_by('timestamp')

    # Handle form submission
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = receiver
            message.save()
            return redirect('chat_room', receiver_id=receiver.id)
    else:
        form = MessageForm()

    # Render the chat room template with context data
    context = {
        'receiver': receiver,
        'messages': messages,
        'form': form,
    }
    return render(request, 'chat/chat_room.html', context)

@login_required
def user_list(request):
    # Fetch all users except the current user
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'chat/user_list.html', {'users': users})