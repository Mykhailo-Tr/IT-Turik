from django import template

register = template.Library()

@register.filter
def is_staff_user(user):

    return user.role in ['admin', 'teacher']