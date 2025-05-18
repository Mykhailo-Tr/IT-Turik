from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages

from accounts.models import Student
from school_system.decorators import parent_required
from dashboard.forms import AddChildForm


@parent_required
def children_view(request):
    children = request.user.parent.children.all()
    form = AddChildForm(user=request.user)

    if request.method == "POST":
        if "add_child" in request.POST:
            form = AddChildForm(request.POST, user=request.user)
            if form.is_valid():
                student = form.cleaned_data['student']
                request.user.parent.children.add(student)
                messages.success(request, f"{student.user.get_full_name()} додано до списку дітей.")
                return redirect("dashboard_children")
        elif "remove_child" in request.POST:
            student_id = request.POST.get("student_id")
            student = get_object_or_404(Student, user__id=student_id)
            request.user.parent.children.remove(student)
            messages.success(request, f"{student.user.get_full_name()} видалено з вашого списку.")
            return redirect("dashboard_children")

    return render(request, 'dashboard/children.html', {
        'form': form,
        'children': children
    })
