document.addEventListener('DOMContentLoaded', function () {
  const calendarEl = document.getElementById('calendar');
  const eventModal = new bootstrap.Modal(document.getElementById('eventModal'));

  const calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    headerToolbar: {
      left: 'prev,next today',
      center: 'title',
      right: 'dayGridMonth,timeGridWeek,timeGridDay'
    },
    editable: true,
    selectable: true,
    navLinks: true,
    events: {
      url: window.calendarData.eventsUrl,
      method: 'GET',
      failure: () => alert('There was an error while fetching events.')
    },
    select: function (info) {
      fetch(`${window.calendarData.eventFormUrl}?start=${info.startStr}&end=${info.endStr}`)
        .then(response => response.text())
        .then(html => {
          document.getElementById('eventModalBody').innerHTML = html;
          eventModal.show();

          const form = document.getElementById('event-form');
          form.addEventListener('submit', function (e) {
            e.preventDefault();
            const formData = new FormData(form);

            fetch(window.calendarData.createEventUrl, {
              method: 'POST',
              body: formData,
              headers: {
                'X-CSRFToken': window.calendarData.csrfToken
              }
            })
            .then(response => response.json())
            .then(data => {
              if (data.success) {
                calendar.refetchEvents();
                eventModal.hide();
              } else {
                document.getElementById('eventModalBody').innerHTML = data.form_html;
              }
            });
          });
        });
      calendar.unselect();
    },
    eventClick: function (info) {
      window.location.href = info.event.url;
    },
    eventDrop: function (info) {
      fetch(`/calendar/events/update/${info.event.id}/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': window.calendarData.csrfToken,
        },
        body: JSON.stringify({
          start: info.event.start.toISOString(),
          end: info.event.end ? info.event.end.toISOString() : info.event.start.toISOString()
        })
      })
      .then(response => response.json())
      .then(() => calendar.refetchEvents());
    }
  });

  calendar.render();
});
