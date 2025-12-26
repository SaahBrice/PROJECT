"""
Accounts App Views
Simple admin authentication.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.translation import gettext_lazy as _


def login_view(request):
    """Admin login page"""
    if request.user.is_authenticated:
        return redirect('admin:index')
    
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        
        # Try to authenticate by email
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
        except User.DoesNotExist:
            user = None
        
        if user is not None and user.is_staff:
            login(request, user)
            messages.success(request, _("Bienvenue !"))
            return redirect('admin:index')
        else:
            messages.error(request, _("Email ou mot de passe incorrect."))
    
    return render(request, 'accounts/login.html')


def logout_view(request):
    """Logout and redirect to home"""
    logout(request)
    messages.info(request, _("Vous avez été déconnecté."))
    return redirect('core:home')
