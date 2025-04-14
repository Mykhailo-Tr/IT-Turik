from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Task, UserTaskStatus
from .forms import CreateTaskForm, EditTaskForm



@login_required(login_url='login')
def tasks_view(request, task_id=None):
    if task_id:
        task = Task.objects.get(id=task_id)
        return render(request, 'tasks/task.html', {'task': task})
        
    context = {
        'page': 'tasks',
        'tasks': Task.objects.all(),
        'user_taken_tasks': UserTaskStatus.objects.filter(user=request.user).values_list('task_id', flat=True),
        'user_completed_tasks': UserTaskStatus.objects.filter(user=request.user, is_completed=True).values_list('task_id', flat=True),
    }
    return render(request, 'tasks/tasks.html', context)


@login_required(login_url='login')
def create_task_view(request):
    if request.method == 'POST':
        form = CreateTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            task.save()
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
def edit_task_view(request, task_id):
    task = Task.objects.get(id=task_id)
    if request.user != task.author:
        messages.error(request, 'You do not have permission to edit this task.')
        return redirect('tasks')
        
    if request.method == 'POST':
        form = CreateTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully.')
            return redirect('tasks')
    else:
        form = CreateTaskForm(instance=task)
        
    context = {
        'page': 'edit_task',
        'form': form,
        'task': task,
    }
    return render(request, 'tasks/forms/edit_task.html', context)


@login_required(login_url='login')
def delete_task_view(request, task_id):
    if request.user != Task.objects.get(id=task_id).author:
        messages.error(request, 'You do not have permission to delete this task.')
        return redirect('tasks')
    task = Task.objects.get(id=task_id)
    task.delete()
    messages.success(request, 'Task deleted successfully.')
    return redirect('tasks')


@login_required(login_url='login')
def take_task_view(request, task_id):
    task = Task.objects.get(id=task_id)
    UserTaskStatus.objects.create(user=request.user, task=task)
    messages.success(request, 'Task taken successfully.')
    return redirect('tasks')


@login_required(login_url='login')
def drop_task_view(request, task_id):
    task = Task.objects.get(id=task_id)
    UserTaskStatus.objects.filter(user=request.user, task=task).delete()
    messages.success(request, 'Task unassigned successfully.')
    return redirect('tasks')


def complete_task_view(request, task_id):
    task = Task.objects.get(id=task_id)
    UserTaskStatus.objects.filter(user=request.user, task=task).update(is_completed=True)
    messages.success(request, 'Task completed successfully.')
    return redirect('tasks')


def uncomplete_task_view(request, task_id):
    task = Task.objects.get(id=task_id)
    UserTaskStatus.objects.filter(user=request.user, task=task).update(is_completed=False)
    messages.success(request, 'Task uncompleted successfully.')
    return redirect('tasks')

