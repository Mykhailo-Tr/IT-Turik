document.addEventListener('DOMContentLoaded', function () {
  const deleteModal = document.getElementById('confirmDeleteModal');
  deleteModal.addEventListener('show.bs.modal', function (event) {
    const button = event.relatedTarget;
    const eventId = button.getAttribute('data-event-id');
    const form = document.getElementById('delete-event-form');
    form.action = `/events/delete/${eventId}/`;
  });
});
