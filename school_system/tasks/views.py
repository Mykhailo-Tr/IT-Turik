from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Task, UserTaskStatus
from .forms import CreateTaskForm, EditTaskForm
from accounts.models import User



@login_required(login_url='login')
def tasks_view(request, task_id=None):
    if task_id:
        task = Task.objects.get(id=task_id)
        return render(request, 'tasks/task.html', {'task': task})
        
    tasks = Task.objects.all().order_by('-date_posted')  # Якщо треба фільтрувати всіх, не лише свої
    users = User.objects.all()
    user_taken_tasks = UserTaskStatus.objects.filter(user=request.user).values_list('task_id', flat=True)
    user_completed_tasks = UserTaskStatus.objects.filter(user=request.user, is_completed=True).values_list('task_id', flat=True)
    
    query = request.GET.get('q')
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    author = request.GET.get('author')
    
    if query:
        tasks = tasks.filter(Q(title__icontains=query) | Q(content__icontains=query)).distinct()
        
    if from_date:
        tasks = tasks.filter(due_date__gte=from_date)
    if to_date:
        tasks = tasks.filter(due_date__lte=to_date)
        
    if author:
        tasks = tasks.filter(author__id=author)        
        
    context = {
        'page': 'tasks',
        'tasks': tasks,
        'users': users,
        'user_taken_tasks': user_taken_tasks,
        'user_completed_tasks': user_completed_tasks,
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


@login_required(login_url='login')
def complete_task_view(request, task_id):
    task = Task.objects.get(id=task_id)
    UserTaskStatus.objects.filter(user=request.user, task=task).update(is_completed=True)
    messages.success(request, 'Task completed successfully.')
    return redirect('tasks')

@login_required(login_url='login')
def uncomplete_task_view(request, task_id):
    task = Task.objects.get(id=task_id)
    UserTaskStatus.objects.filter(user=request.user, task=task).update(is_completed=False)
    messages.success(request, 'Task uncompleted successfully.')
    return redirect('tasks')

