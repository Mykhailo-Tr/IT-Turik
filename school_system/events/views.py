from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from django.utils.timezone import now
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from .models import Event, EventParticipation, EventComment
from .forms import CreateEventForm
from accounts.models import User


class EventListView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, event_id=None):
        if event_id:
            return self.get_event_detail(request, event_id)

        created_events = Event.objects.filter(author=request.user) if request.user.role != 'admin' else Event.objects.all()
        invited_events = Event.objects.filter(eventparticipation__user=request.user).exclude(author=request.user)

        q = request.GET.get('q', '').strip()
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')
        time_filter = request.GET.get('time')
        status = request.GET.get('status')
        author = request.GET.get('author')

        if q:
            invited_events = invited_events.filter(
                Q(title__icontains=q) | Q(author__first_name__icontains=q) | Q(author__last_name__icontains=q)
            )
        if from_date:
            invited_events = invited_events.filter(start_date__date__gte=from_date)
        if to_date:
            invited_events = invited_events.filter(end_date__date__lte=to_date)
        if time_filter == 'future':
            invited_events = invited_events.filter(start_date__gte=now())
        elif time_filter == 'past':
            invited_events = invited_events.filter(end_date__lt=now())
        if status:
            invited_events = invited_events.filter(eventparticipation__user=request.user,
                                                   eventparticipation__response=status)
        if author:
            invited_events = invited_events.filter(author__id=author)

        participations = {
            p.event_id: p.response for p in EventParticipation.objects.filter(user=request.user)
        }
        users = User.objects.all()

        context = {
            "created_events": created_events,
            "invited_events": invited_events,
            "participations": participations,
            "users": users,
            "page": "events",
            "filter": {
                "q": q,
                "from_date": from_date,
                "to_date": to_date,
                "status": status,
                "time": time_filter
            }
        }

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return render(request, 'events/event_list_partial.html', context)

        return render(request, 'events/events.html', context)

    def get_event_detail(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        participation = EventParticipation.objects.filter(event=event, user=request.user).first()
        comments = EventComment.objects.filter(event=event)
        return render(request, 'events/event_details.html', {
            "event": event,
            "participation": participation,
            "comments": comments,
            "page": "event_details"
        })


class EventCommentAddView(LoginRequiredMixin, View):
    def post(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)

        is_author = event.author == request.user
        participation = EventParticipation.objects.filter(
            event=event, user=request.user,
            response=EventParticipation.ResponseChoices.ACCEPTED
        ).first()

        if not (participation or is_author):
            messages.error(request, "Only participants who accepted the event or the author can comment.")
            return redirect('event_details', event_id=event.id)

        comment_text = request.POST.get('comment', '').strip()
        if comment_text:
            EventComment.objects.create(user=request.user, event=event, comment=comment_text)

        return redirect('event_details', event_id=event.id)


class EventCommentDeleteView(LoginRequiredMixin, View):
    def post(self, request, comment_id):
        comment = get_object_or_404(EventComment, id=comment_id)
        event = comment.event

        if comment.user != request.user and event.author != request.user:
            messages.error(request, "You don't have permission to delete this comment.")
            return redirect('event_details', event_id=event.id)

        comment.delete()
        messages.success(request, "Comment deleted successfully.")
        return redirect('event_details', event_id=event.id)


class RespondToEventView(LoginRequiredMixin, View):
    def post(self, request, event_id, response):
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


class LeaveEventView(LoginRequiredMixin, View):
    def post(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        participation = get_object_or_404(EventParticipation, user=request.user, event=event)

        if participation.response == EventParticipation.ResponseChoices.ACCEPTED:
            participation.response = EventParticipation.ResponseChoices.LEAVED
            participation.save()
            messages.success(request, "You have left the event.")
        else:
            messages.warning(request, "You can only leave an event you have accepted.")
        return redirect('events')


class EventCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = CreateEventForm(user=request.user)
        return render(request, 'events/forms/event_form.html', {'form': form})

    def post(self, request):
        form = CreateEventForm(request.POST, user=request.user)
        if form.is_valid():
            event = form.save(commit=False)
            event.author = request.user
            event.save()
            form.save_m2m()

            for user in form.cleaned_data['participants']:
                EventParticipation.objects.create(event=event, user=user)

            return redirect('events')
        return render(request, 'events/forms/event_form.html', {'form': form})


class EventEditView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.get_object().author == self.request.user

    def get_object(self):
        return get_object_or_404(Event, id=self.kwargs['event_id'])

    def get(self, request, event_id):
        event = self.get_object()
        form = CreateEventForm(instance=event)
        selected_participants = User.objects.filter(eventparticipation__event=event)

        form.initial['participants'] = selected_participants
        form.fields['participants'].queryset = (
            User.objects.exclude(id=request.user.id) | selected_participants
        ).distinct()

        return render(request, 'events/forms/event_form.html', {
            'form': form, 'event': event, 'page': 'edit_event'
        })

    def post(self, request, event_id):
        event = self.get_object()
        form = CreateEventForm(request.POST, instance=event)

        if form.is_valid():
            event = form.save(commit=False)
            event.author = request.user
            event.save()
            form.save_m2m()

            selected_participants = form.cleaned_data['participants']
            current_participants = User.objects.filter(eventparticipation__event=event)

            for user in current_participants:
                if user not in selected_participants:
                    EventParticipation.objects.filter(event=event, user=user).delete()
            for user in selected_participants:
                EventParticipation.objects.get_or_create(event=event, user=user)

            messages.success(request, 'Event updated successfully.')
            return redirect('events')

        return render(request, 'events/forms/event_form.html', {
            'form': form, 'event': event, 'page': 'edit_event'
        })


class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        event = get_object_or_404(Event, id=self.kwargs['event_id'])
        return event.author == self.request.user

    def post(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        event.delete()
        messages.success(request, 'Event deleted successfully.')
        return redirect('events')
