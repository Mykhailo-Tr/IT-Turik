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
        return render(request, 'events/event_details.html', {
            "event": event,
            "participation": participation,
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


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def create_event_view(request):
    if request.method == 'POST':
        form = CreateEventForm(request.POST)
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
        form = CreateEventForm()

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
        if form.is_valid():
            event = form.save(commit=False)
            event.author = request.user
            event.save()
            form.save_m2m()

            selected_participants = form.cleaned_data['participants']
            current_participants = User.objects.filter(eventparticipation__event=event)

            # Видаляємо учасників, яких зняли з події
            for user in current_participants:
                if user not in selected_participants:
                    EventParticipation.objects.filter(event=event, user=user).delete()

            # Додаємо нових учасників
            for user in selected_participants:
                EventParticipation.objects.get_or_create(event=event, user=user)

            messages.success(request, 'Event updated successfully.')
            return redirect('events')
    else:
        form = CreateEventForm(instance=event)

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