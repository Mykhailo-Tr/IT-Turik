from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.utils.timezone import make_aware, is_naive
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string

from events.models import Event
from events.forms import CreateEventForm

from datetime import datetime
import json


class FullCalendarView(LoginRequiredMixin, TemplateView):
    template_name = "calendarapp/calendar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CreateEventForm(user=self.request.user)
        context["page"] = "calendar"
        return context


class EventListJsonView(LoginRequiredMixin, View):
    def get(self, request):
        user_events = Event.objects.filter(author=request.user).exclude(end_date__isnull=True)
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


class EventFormPartialView(LoginRequiredMixin, View):
    def get(self, request, event_id=None):
        event = get_object_or_404(Event, id=event_id) if event_id else None
        form = CreateEventForm(instance=event)
        return render(request, 'calendarapp/event_form_partial.html', {'form': form, 'event': event})


class CreateEventView(LoginRequiredMixin, View):
    def post(self, request):
        form = CreateEventForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            event = form.save(commit=False)
            event.author = request.user
            event.save()
            form.save_m2m()
            return JsonResponse({"success": True})
        return JsonResponse({
            "success": False,
            "form_html": render_to_string("calendarapp/event_form_partial.html", {"form": form}, request=request)
        })


class UpdateEventDateView(LoginRequiredMixin, View):
    def post(self, request, event_id):
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
            return JsonResponse({"error": str(e)}, status=500)


class DeleteEventView(LoginRequiredMixin, View):
    def get(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        if request.user != event.author:
            messages.error(request, 'You do not have permission to delete this event.')
        else:
            event.delete()
            messages.success(request, 'Event deleted successfully.')
        return redirect('calendarapp:calendar')
