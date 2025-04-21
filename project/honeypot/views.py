from django.shortcuts import render
from django.utils import timezone
from .models import HoneypotLog

def honeypot_login(request):
    if request.method == 'POST':
        ip_address = request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR')
        HoneypotLog.objects.create(
            timestamp=timezone.now(),
            username=request.user, 
            ipv4_address=ip_address, 
            post_params=dict(request.POST)
        )
        return render(request, 'admin_login.html', {
            'error_message': "Please enter the correct username and password.",
        })

    return render(request, 'admin_login.html')