from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from accounts.models import Subject
from school_system.decorators import teacher_required
from ..forms import AddSubjectForm


@method_decorator(teacher_required, name='dispatch')
class SubjectsView(View):
    def get(self, request):
        form = AddSubjectForm(user=request.user)
        subjects = Subject.objects.all()
        my_subjects = request.user.teacher.subjects.all()
        return render(request, 'dashboard/subjects.html', {
            'form': form,
            'subjects': subjects,
            'my_subjects': my_subjects,
        })

    def post(self, request):
        form = AddSubjectForm(request.POST, user=request.user)
        if form.is_valid():
            subject = form.save()
            request.user.teacher.subjects.add(subject)
            messages.success(request, "Subject added and assigned successfully.")
        else:
            messages.error(request, "There was an error adding the subject.")
        return redirect("dashboard_subjects")


@method_decorator(teacher_required, name='dispatch')
class AttachSubjectView(View):
    def get(self, request, subject_id):
        subject = get_object_or_404(Subject, id=subject_id)
        request.user.teacher.subjects.add(subject)
        messages.success(request, f"Subject '{subject.name}' attached to you.")
        return redirect('dashboard_subjects')


@method_decorator(teacher_required, name='dispatch')
class DetachSubjectView(View):
    def get(self, request, subject_id):
        subject = get_object_or_404(Subject, id=subject_id)
        request.user.teacher.subjects.remove(subject)
        messages.success(request, f"Subject '{subject.name}' detached from you.")
        return redirect('dashboard_subjects')


@method_decorator(teacher_required, name='dispatch')
class DeleteSubjectView(View):
    def get(self, request, subject_id):
        subject = get_object_or_404(Subject, id=subject_id)
        return render(request, 'dashboard/confirm_delete_subject.html', {'subject': subject})

    def post(self, request, subject_id):
        subject = get_object_or_404(Subject, id=subject_id)
        if request.user.role != 'admin' and subject not in request.user.teacher.subjects.all():
            messages.error(request, "You don't have permission to delete this subject.")
        else:
            subject.delete()
            messages.success(request, "Subject deleted successfully.")
        return redirect('dashboard_subjects')
