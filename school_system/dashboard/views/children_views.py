from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404, render

from accounts.models import Student
from school_system.decorators import parent_required
from ..forms import AddChildForm


@parent_required
def children_view(request):
    children = request.user.parent.children.all()
    form = AddChildForm(user=request.user)
    return render(request, 'dashboard/children.html', {'form': form, 'children': children})

    
@login_required
def add_child_ajax(request):
    if request.method == 'POST':
        form = AddChildForm(request.POST, user=request.user)
        if form.is_valid():
            child = form.cleaned_data['child']
            request.user.parent.children.add(child)
    html = render_to_string('accounts/partials/children_list.html', {'user': request.user})
    return JsonResponse({'html': html})


@login_required
def remove_child_ajax(request):
    if request.method == 'POST':
        child_id = request.POST.get('child_id')
        child = get_object_or_404(Student, user_id=child_id)
        request.user.parent.children.remove(child)
    html = render_to_string('accounts/partials/children_list.html', {'user': request.user})
    return JsonResponse({'html': html})

