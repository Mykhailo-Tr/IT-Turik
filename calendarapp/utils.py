from calendar import HTMLCalendar
from django.urls import reverse
from events.models import Event

class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    def formatday(self, day, events):
        events_per_day = events.filter(start_date__day=day)
        d = ""
        for event in events_per_day:
            d += f'<li><a href="{reverse("event_details", args=[event.id])}">{event.title}</a></li>'
        if day != 0:
            return f"<td><span class='date'>{day}</span><ul>{d}</ul></td>"
        return "<td></td>"

    def formatweek(self, theweek, events):
        week = ""
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f"<tr>{week}</tr>"

    def formatmonth(self, withyear=True):
        events = Event.objects.filter(start_date__year=self.year, start_date__month=self.month)
        cal = f"""<table class="calendar"> 
<thead>
<tr>{self.formatmonthname(self.year, self.month, withyear=withyear)}</tr>
<tr>{self.formatweekheader()}</tr>
</thead>
<tbody>"""
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f"\n{self.formatweek(week, events)}"
        cal += "</tbody></table>"
        return cal
