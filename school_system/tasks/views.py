from django.shortcuts import render, redirect
from .models import Task
from .forms import CreateTaskForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def tasks_view(request, task_id=None):
    if task_id:
        task = Task.objects.get(id=task_id)
        return render(request, 'tasks/task.html', {'task': task})
        
    context = {
        'page': 'tasks',
        'tasks': Task.objects.all(),
    }
    return render(request, 'tasks/tasks.html', context)


@login_required(login_url='login')
def create_task_view(request):
    if request.method == 'POST':
        form = CreateTaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task created successfully.')
            return redirect('tasks')
    else:
        form = CreateTaskForm()
        
    context = {
        'page': 'create_task',
        'form': form,
    }
    return render(request, 'tasks/forms/create_task.html', context)


@login_required(login_url='login')
def delete_task_view(request, task_id):
    task = Task.objects.get(id=task_id)
    task.delete()
    messages.success(request, 'Task deleted successfully.')
    return redirect('tasks')

