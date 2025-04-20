from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
    if ip_address:
        ip_address = ip_address.split(',')[0]
    else:
        ip_address = request.META.get('REMOTE_ADDR')

    print(ip_address)
    print(request.user)
    print(request.method + " " + request.path)
    print(request.body)
    print(request.GET)
    print(request.POST)

    return HttpResponse(f'<h1>Honeypot!</h1>')