from django.views.generic import TemplateView, ListView, FormView, DeleteView
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from school_system.decorators import teacher_required
from accounts.models import User
from accounts.forms import StudentSignUpForm, TeacherSignUpForm, ParentSignUpForm



@method_decorator(login_required(login_url='login'), name='dispatch')
class DashboardView(TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'dashboard'
        return context


@method_decorator(login_required(login_url='login'), name='dispatch')
class AccountsView(ListView):
    model = User
    template_name = 'dashboard/accounts.html'
    context_object_name = 'accounts'

    def get_queryset(self):
        queryset = User.objects.exclude(id=self.request.user.id)
        if self.request.user.role in ['student', 'parent']:
            queryset = queryset.exclude(role='admin')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(email__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'dashboard'
        context['accounts_count'] = context['accounts'].count()
        return context


@method_decorator(teacher_required(login_url='login'), name='dispatch')
class CreateAccountView(FormView):
    template_name = 'dashboard/forms/create_user.html'

    def dispatch(self, request, *args, **kwargs):
        self.role = kwargs.get('role')
        return super().dispatch(request, *args, **kwargs)

    def get_form_class(self):
        if self.role == 'student':
            return StudentSignUpForm
        elif self.role == 'parent':
            return ParentSignUpForm
        elif self.role == 'teacher':
            return TeacherSignUpForm
        else:
            messages.error(self.request, 'Невідома роль.')
            return None

    def get_form(self, form_class=None):
        form_class = self.get_form_class()
        return form_class(self.request.POST or None)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, f'{self.role.capitalize()} успішно створено.')
        return redirect('dashboard_accounts')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'dashboard'
        context['role'] = self.role
        return context
