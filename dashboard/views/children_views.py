from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from accounts.models import Student
from school_system.decorators import parent_required
from dashboard.forms import AddChildForm


@method_decorator(parent_required, name='dispatch')
class ChildrenView(View):
    def get(self, request):
        form = AddChildForm(user=request.user)
        children = request.user.parent.children.all()
        return render(request, 'dashboard/children.html', {'form': form, 'children': children})

    def post(self, request):
        form = AddChildForm(request.POST, user=request.user)
        if "add_child" in request.POST and form.is_valid():
            student = form.cleaned_data['student']
            request.user.parent.children.add(student)
            messages.success(request, f"{student.user.get_full_name()} додано до списку дітей.")
        elif "remove_child" in request.POST:
            student_id = request.POST.get("student_id")
            student = get_object_or_404(Student, user__id=student_id)
            request.user.parent.children.remove(student)
            messages.success(request, f"{student.user.get_full_name()} видалено з вашого списку.")
        return redirect("dashboard_children")
