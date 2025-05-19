from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils import timezone
from django.urls import reverse_lazy
from django.db.models import Q
from datetime import date

from .models import Task, UserTaskStatus
from .forms import TaskForm
from accounts.models import User


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/tasks.html'
    context_object_name = 'tasks'
    login_url = 'login'

    def get_queryset(self):
        tasks = Task.objects.all().order_by('-date_posted')
        request = self.request

        query = request.GET.get('q')
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')
        author = request.GET.get('author')
        today_only = request.GET.get('today')
        status_filter = request.GET.get('status')

        if query:
            tasks = tasks.filter(Q(title__icontains=query) | Q(content__icontains=query))

        if from_date:
            tasks = tasks.filter(due_date__gte=from_date)
        if to_date:
            tasks = tasks.filter(due_date__lte=to_date)

        if today_only == "1":
            tasks = tasks.filter(due_date__date=date.today())

        if author:
            tasks = tasks.filter(author__id=author)

        if status_filter == "completed":
            tasks = tasks.filter(usertaskstatus__user=request.user, usertaskstatus__is_completed=True)
        elif status_filter == "incomplete":
            tasks = tasks.filter(usertaskstatus__user=request.user).exclude(usertaskstatus__is_completed=True)

        return tasks.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        context['page'] = 'tasks'
        context['users'] = User.objects.all()
        context['user_taken_tasks'] = UserTaskStatus.objects.filter(user=request.user).values_list('task_id', flat=True)
        context['user_completed_tasks'] = UserTaskStatus.objects.filter(user=request.user, is_completed=True).values_list('task_id', flat=True)
        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task.html'
    context_object_name = 'task'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'task'
        context['user_taken_tasks'] = UserTaskStatus.objects.filter(user=self.request.user).values_list('task_id', flat=True)
        context['user_completed_tasks'] = UserTaskStatus.objects.filter(user=self.request.user, is_completed=True).values_list('task_id', flat=True)
        return context


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/forms/task_form.html'
    success_url = reverse_lazy('tasks')
    login_url = 'login'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Task created successfully.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'create_task'
        return context


class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/forms/task_form.html'
    success_url = reverse_lazy('tasks')
    login_url = 'login'

    def form_valid(self, form):
        messages.success(self.request, 'Task updated successfully.')
        return super().form_valid(form)

    def test_func(self):
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, 'You do not have permission to edit this task.')
        return redirect('tasks')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'edit_task'
        return context


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('tasks')
    login_url = 'login'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = self.object
        return context
    
    def get(self, request, *args, **kwargs):
        messages.success(request, 'Task deleted successfully.')
        return super().delete(request, *args, **kwargs)

    def test_func(self):
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, 'You do not have permission to delete this task.')
        return redirect('tasks')


class ToggleTaskCompletionView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        status, _ = UserTaskStatus.objects.get_or_create(user=request.user, task=task)
        status.is_completed = not status.is_completed
        status.completed_at = timezone.now() if status.is_completed else None
        status.save()
        return redirect('tasks')


class ToggleTaskParticipationView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        status, created = UserTaskStatus.objects.get_or_create(user=request.user, task=task)
        if not created:
            status.delete()
        else:
            status.is_completed = False
            status.save()
        return redirect('tasks')
