from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from accounts.models import Subject
from school_system.decorators import teacher_required
from ..forms import AddSubjectForm


@teacher_required
def subjects_view(request):
    form = AddSubjectForm(user=request.user)
    subjects = Subject.objects.all()
    my_subjects = request.user.teacher.subjects.all()

    if request.method == "POST":
        form = AddSubjectForm(request.POST, user=request.user)
        if form.is_valid():
            subject = form.save()
            request.user.teacher.subjects.add(subject)
            messages.success(request, "Subject added and assigned successfully.")
            return redirect("dashboard_subjects")
        else:
            messages.error(request, "There was an error adding the subject.")

    return render(request, 'dashboard/subjects.html', {
        'form': form,
        'subjects': subjects,
        'my_subjects': my_subjects,
    })


@teacher_required
def attach_subject_view(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    request.user.teacher.subjects.add(subject)
    messages.success(request, f"Subject '{subject.name}' attached to you.")
    return redirect('dashboard_subjects')


@teacher_required
def detach_subject_view(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    request.user.teacher.subjects.remove(subject)
    messages.success(request, f"Subject '{subject.name}' detached from you.")
    return redirect('dashboard_subjects')


@teacher_required
def delete_subject_view(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)

    if request.user.role != 'admin' and subject not in request.user.teacher.subjects.all():
        messages.error(request, "You don't have permission to delete this subject.")
        return redirect('dashboard_subjects')

    if request.method == "POST":
        subject.delete()
        messages.success(request, "Subject deleted successfully.")
        return redirect('dashboard_subjects')

    return render(request, 'dashboard/confirm_delete_subject.html', {
        'subject': subject
    })

