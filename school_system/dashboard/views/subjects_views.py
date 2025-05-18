from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404

from accounts.models import Subject
from ..forms import AddSubjectForm



@login_required
def add_subject_ajax(request):
    if request.method == 'POST':
        form = AddSubjectForm(request.POST, user=request.user)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            request.user.teacher.subjects.add(subject)
    html = render_to_string('accounts/partials/subjects_list.html', {'user': request.user})
    return JsonResponse({'html': html})


@login_required
def remove_subject_ajax(request):
    if request.method == 'POST':
        subject_id = request.POST.get('subject_id')
        subject = get_object_or_404(Subject, id=subject_id)
        request.user.teacher.subjects.remove(subject)
    html = render_to_string('accounts/partials/subjects_list.html', {'user': request.user})
    return JsonResponse({'html': html})

