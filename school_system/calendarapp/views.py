from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.utils.safestring import mark_safe
from datetime import datetime, date, timedelta
import calendar
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from events.models import Event, EventParticipation
from django.urls import reverse
from calendarapp.utils import Calendar
from events.forms import CreateEventForm


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split("-"))
        return date(year, month, 1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    return f"month={prev_month.year}-{prev_month.month}"

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    return f"month={next_month.year}-{next_month.month}"


class CalendarView(View):
    def get(self, request):
        view_mode = request.GET.get("view", "month")  # default 'month'
        d = get_date(request.GET.get("month", None))

        events = Event.objects.filter(start_date__year=d.year, start_date__month=d.month)

        if view_mode == "week":
            week_start = d - timedelta(days=d.weekday())
            week_end = week_start + timedelta(days=6)
            events = events.filter(start_date__date__range=(week_start, week_end))
            title = f"Week of {week_start.strftime('%B %d, %Y')}"
            html = self.render_week(week_start, events)
        elif view_mode == "day":
            events = events.filter(start_date__date=d)
            title = d.strftime('%A, %B %d, %Y')
            html = self.render_day(d, events)
        else:
            cal = Calendar(d.year, d.month)
            html = cal.formatmonth(withyear=True)
            title = d.strftime('%B %Y')

        context = {
            "calendar": mark_safe(html),
            "prev_month": prev_month(d),
            "next_month": next_month(d),
            "view_mode": view_mode,
            "title": title
        }
        return render(request, "calendarapp/calendar.html", context)

    def render_week(self, start_date, events):
        html = "<table class='table'><tr>"
        for i in range(7):
            day = start_date + timedelta(days=i)
            day_events = events.filter(start_date__day=day.day)
            html += f"<td><strong>{day.strftime('%A')} {day.day}</strong><ul>"
            for e in day_events:
                html += f'<li><a href="{reverse("event_details", args=[e.id])}">{e.title}</a></li>'
            html += "</ul></td>"
        html += "</tr></table>"
        return html

    def render_day(self, day, events):
        html = f"<h5>{day.strftime('%A, %B %d, %Y')}</h5><ul>"
        for e in events:
            html += f'<li><a href="{reverse("event_details", args=[e.id])}">{e.title}</a> ({e.start_date.strftime("%H:%M")})</li>'
        html += "</ul>"
        return html


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

            return redirect('calendarapp:calendar')
    else:
        form = CreateEventForm(user=request.user)

    return render(request, 'events/forms/create.html', {'form': form})


@login_required(login_url="login")
def event_details(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    eventmember = EventParticipation.objects.filter(event=event_id)
    context = {"event": event, "eventmember": eventmember}
    return render(request, "events/event_details.html", context)


@login_required(login_url="login")
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.user != event.author:
        messages.error(request, 'You do not have permission to delete this event.')
        return redirect('calendarapp:calendar')
    event.delete()
    messages.success(request, 'Event deleted successfully.')
    return redirect('calendarapp:calendar')
