from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def login_redirect(request):
    if request.user.is_superuser or request.user.is_staff:
        return redirect('admin')
    return redirect('medical')
