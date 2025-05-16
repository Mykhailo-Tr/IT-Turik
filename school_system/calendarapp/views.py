# calendarapp/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.utils.timezone import make_aware, is_naive
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from datetime import datetime

from events.models import Event, EventParticipation
from events.forms import CreateEventForm

import json


class FullCalendarView(LoginRequiredMixin, View):
    def get(self, request):
        form = CreateEventForm(user=request.user)
        return render(request, "calendarapp/fullcalendar.html", {"form": form})


def get_events_json(request):
    user_events = Event.objects.filter(author=request.user)
    event_list = [
        {
            "id": event.id,
            "title": event.title,
            "start": event.start_date.isoformat(),
            "end": event.end_date.isoformat(),
            "url": f"/events/{event.id}/",
        }
        for event in user_events
    ]
    return JsonResponse(event_list, safe=False)


@login_required(login_url="login")
def create_event(request):
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

            return redirect('calendarapp:fullcalendar')
    return redirect('calendarapp:fullcalendar')


@login_required(login_url="login")
def update_event_date(request, event_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            event = get_object_or_404(Event, id=event_id, author=request.user)

            start = datetime.fromisoformat(data.get("start"))
            end = datetime.fromisoformat(data.get("end"))

            if is_naive(start):
                start = make_aware(start)
            if is_naive(end):
                end = make_aware(end)

            event.start_date = start
            event.end_date = end
            event.save()

            return JsonResponse({"message": "Event updated successfully."})
        except Exception as e:
            print(f"Error updating event: {e}")
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request."}, status=400)


@login_required(login_url="login")
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.user != event.author:
        messages.error(request, 'You do not have permission to delete this event.')
        return redirect('calendarapp:fullcalendar')
    event.delete()
    messages.success(request, 'Event deleted successfully.')
    return redirect('calendarapp:fullcalendar')
