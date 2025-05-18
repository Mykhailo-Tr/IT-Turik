from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Task, UserTaskStatus
from .forms import TaskForm
from accounts.models import User
from datetime import date, datetime




@login_required(login_url='login')
def tasks_view(request, task_id=None):
    user_taken_tasks = UserTaskStatus.objects.filter(user=request.user).values_list('task_id', flat=True)
    user_completed_tasks = UserTaskStatus.objects.filter(user=request.user, is_completed=True).values_list('task_id', flat=True)

    if task_id:
        task = get_object_or_404(Task, id=task_id)
        context = {
            'page': 'task',
            'task': task,
            'user_taken_tasks': user_taken_tasks,
            'user_completed_tasks': user_completed_tasks,
        }
        return render(request, 'tasks/task.html', context)

    tasks = Task.objects.all().order_by('-date_posted')
    users = User.objects.all()

    query = request.GET.get('q')
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    author = request.GET.get('author')
    today_only = request.GET.get('today')
    status_filter = request.GET.get('status')

    if query:
        tasks = tasks.filter(Q(title__icontains=query) | Q(content__icontains=query)).distinct()

    if from_date:
        tasks = tasks.filter(due_date__gte=from_date)
    if to_date:
        tasks = tasks.filter(due_date__lte=to_date)

    if today_only == "1":
        today = date.today()
        tasks = tasks.filter(due_date__date=today)

    if author:
        tasks = tasks.filter(author__id=author)

    if status_filter == "completed":
        tasks = tasks.filter(usertaskstatus__user=request.user, usertaskstatus__is_completed=True)
    elif status_filter == "incomplete":
        tasks = tasks.filter(usertaskstatus__user=request.user).exclude(usertaskstatus__is_completed=True)

    context = {
        'page': 'tasks',
        'tasks': tasks.distinct(),
        'users': users,
        'user_taken_tasks': user_taken_tasks,
        'user_completed_tasks': user_completed_tasks,

    }
    return render(request, 'tasks/tasks.html', context)

@login_required(login_url='login')
def create_task_view(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            task.save()
            messages.success(request, 'Task created successfully.')
            return redirect('tasks')
    else:
        form = TaskForm()
        
    context = {
        'page': 'create_task',
        'form': form,
    }
    return render(request, 'tasks/forms/task_form.html', context)


@login_required(login_url='login')
def edit_task_view(request, task_id):
    task = Task.objects.get(id=task_id)
    if request.user != task.author:
        messages.error(request, 'You do not have permission to edit this task.')
        return redirect('tasks')
        
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully.')
            return redirect('tasks')
    else:
        form = TaskForm(instance=task)
        
    context = {
        'page': 'edit_task',
        'form': form,
        'task': task,
    }
    return render(request, 'tasks/forms/task_form.html', context)


@login_required(login_url='login')
def delete_task_view(request, task_id):
    if request.user != Task.objects.get(id=task_id).author:
        messages.error(request, 'You do not have permission to delete this task.')
        return redirect('tasks')
    task = Task.objects.get(id=task_id)
    task.delete()
    messages.success(request, 'Task deleted successfully.')
    return redirect('tasks')


@login_required
def toggle_task_completion_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    status, _ = UserTaskStatus.objects.get_or_create(user=request.user, task=task)
    status.is_completed = not status.is_completed
    status.completed_at = timezone.now() if status.is_completed else None
    status.save()
    return redirect('tasks')


@login_required
def toggle_task_participation(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    status, created = UserTaskStatus.objects.get_or_create(user=request.user, task=task)

    if not created:
        status.delete()
    else:
        status.is_completed = False
        status.save()

    return redirect('tasks')
