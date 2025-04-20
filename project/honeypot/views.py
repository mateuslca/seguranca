from django.shortcuts import render
from django.http import HttpResponse
from .models import HoneypotLog

def home(request):
    ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
    if ip_address:
        ip_address = ip_address.split(',')[0]
    else:
        ip_address = request.META.get('REMOTE_ADDR')

    log = HoneypotLog.objects.create(
        username=request.user, 
        ipv4_address=ip_address, 
        ipv6_address=ip_address, 
        action=request.method + " " + request.path, 
        get_params=request.GET,
        post_params= request.POST
    )

    return HttpResponse(f'<h1>Honeypot!</h1>')