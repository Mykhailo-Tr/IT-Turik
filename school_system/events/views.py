from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.shortcuts import get_object_or_404
from .models import Event, EventParticipation, EventComment
from .forms import CreateEventForm
from accounts.models import User


@login_required(login_url='login')
def events_view(request, event_id=None):
    if event_id:
        event = get_object_or_404(Event, id=event_id)
        participation = EventParticipation.objects.filter(event=event, user=request.user).first()
        comments = EventComment.objects.filter(event=event)
        return render(request, 'events/event_details.html', {
            "event": event,
            "participation": participation,
            "comments": comments,
            "page": "event_details"
        })

    if request.user.role == 'admin':
        created_events = Event.objects.all()
        invited_events = Event.objects.none()
    else:
        created_events = Event.objects.filter(author=request.user)
        invited_events = Event.objects.filter(eventparticipation__user=request.user).exclude(author=request.user)

    participations = {
        p.event_id: p.response for p in EventParticipation.objects.filter(user=request.user)
    }

    return render(request, 'events/events.html', {
        "created_events": created_events,
        "invited_events": invited_events,
        "participations": participations,
        "page": "events"
    })
    
@login_required(login_url='login')
@require_POST
def add_event_comment(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    is_author = event.author == request.user
    participation = EventParticipation.objects.filter(
        event=event,
        user=request.user,
        response=EventParticipation.ResponseChoices.ACCEPTED
    ).first()

    if not (participation or is_author):
        messages.error(request, "Only participants who accepted the event or the author can comment.")
        return redirect('event_details', event_id=event.id)

    comment_text = request.POST.get('comment', '').strip()
    if comment_text:
        EventComment.objects.create(user=request.user, event=event, comment=comment_text)

    return redirect('event_details', event_id=event.id)



@login_required
@require_POST
def delete_event_comment(request, comment_id):
    comment = get_object_or_404(EventComment, id=comment_id)
    event = comment.event

    is_author = event.author == request.user
    is_comment_owner = comment.user == request.user

    if not (is_comment_owner or is_author):
        messages.error(request, "You don't have permission to delete this comment.")
        return redirect('event_details', event_id=event.id)

    comment.delete()
    messages.success(request, "Comment deleted successfully.")
    return redirect('event_details', event_id=event.id)

    
    
@login_required
@require_POST
def respond_to_event(request, event_id, response):
    event = get_object_or_404(Event, id=event_id)
    if not EventParticipation.objects.filter(event=event, user=request.user).exists():
        messages.error(request, "You are not invited to this event.")
        return redirect('events')

    if response not in [choice[0] for choice in EventParticipation.ResponseChoices.choices]:
        messages.error(request, "Invalid response.")
        return redirect('events')

    participation = EventParticipation.objects.get(event=event, user=request.user)
    participation.response = response
    participation.save()
    messages.success(request, f"You have {response} the event.")
    return redirect('events')


@login_required
@require_POST
def leave_event_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    participation = get_object_or_404(EventParticipation, user=request.user, event=event)

    if participation.response == EventParticipation.ResponseChoices.ACCEPTED:
        participation.response = EventParticipation.ResponseChoices.LEAVED
        participation.save()
        messages.success(request, "You have left the event.")
    else:
        messages.warning(request, "You can only leave an event you have accepted.")

    return redirect('events')


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def create_event_view(request):
    if request.method == 'POST':
        form = CreateEventForm(request.POST, user=request.user)
        if form.is_valid():
            event = form.save(commit=False)
            event.author = request.user
            event.save()
            form.save_m2m()

            participants = form.cleaned_data['participants']
            for user in participants:
                EventParticipation.objects.create(event=event, user=user)

            return redirect('events')
    else:
        form = CreateEventForm(user=request.user)

    return render(request, 'events/forms/create.html', {'form': form})


@login_required(login_url="login")
@require_http_methods(["GET", "POST"])
def edit_event_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.user != event.author:
        messages.error(request, 'You do not have permission to edit this event.')
        return redirect('events')

    if request.method == 'POST':
        form = CreateEventForm(request.POST, instance=event)
        print(form)
        if form.is_valid():
            event = form.save(commit=False)
            event.author = request.user
            event.save()
            form.save_m2m()

            selected_participants = form.cleaned_data['participants']
            current_participants = User.objects.filter(eventparticipation__event=event)
            print(selected_participants, current_participants)

            for user in current_participants:
                if user not in selected_participants:
                    EventParticipation.objects.filter(event=event, user=user).delete()

            for user in selected_participants:
                EventParticipation.objects.get_or_create(event=event, user=user)

            messages.success(request, 'Event updated successfully.')
            return redirect('events')
    else:
        form = CreateEventForm(instance=event)

        selected_participants = User.objects.filter(eventparticipation__event=event)

        form.initial['participants'] = selected_participants

        form.fields['participants'].queryset = (
            User.objects.exclude(id=request.user.id) | selected_participants
        ).distinct()


    form.fields['participants'].queryset = User.objects.exclude(id=request.user.id)

    context = {
        'page': 'edit_event',
        'form': form,
        'event': event,
    }
    return render(request, 'events/forms/edit.html', context)



@login_required(login_url="login")
@require_http_methods(["GET", "POST"])
def delete_event_view(request, event_id):
    if request.user != Event.objects.get(id=event_id).author:
        messages.error(request, 'You do not have permission to delete this event.')
        return redirect('events')
    event = Event.objects.get(id=event_id)
    event.delete()
    messages.success(request, 'Event deleted successfully.')
    return redirect('events')

