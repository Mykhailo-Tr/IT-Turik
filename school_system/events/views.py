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
@require_GET
def events_view(request, event_id=None):
    if event_id:
        event = get_object_or_404(Event, id=event_id)
        return render(request, 'events/event_details.html', {"event": event, "page": "event_details"})

    events = Event.objects.all()
    return render(request, 'events/events.html', {"events": events})


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def create_event_view(request):
    if request.method == 'POST':
        form = CreateEventForm(request.POST)
        if form.is_valid():
            # Зберігаємо подію без багатьох до багатьох полів
            event = form.save(commit=False)
            event.author = request.user
            event.save()  # Збереження події без учасників
            
            # Зберігаємо Many-to-Many (tasks) після збереження події
            form.save_m2m()

            # Додаємо учасників через модель EventParticipation
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
    event = Event.objects.get(id=event_id)
    
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