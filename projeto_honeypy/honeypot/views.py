import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
import pandas as pd
from django.views.decorators.csrf import csrf_exempt

# Caminho para os logs
base_dir = Path(__file__).resolve().parent.parent
http_log_path = base_dir / 'log_files' / 'http_audit.log'

@csrf_exempt
def simple_dashboard(request):
    # Leitura básica dos logs
    try:
        colnames=['date', 'ip_address', 'username', 'password'] 
        http_df = pd.read_csv(http_log_path, names=colnames)

        
        print(http_df.head())
        print("\n"*10)
        print("-"*10)

    except Exception as e:
        return render(request, "dashboard.html", {
            "error": f"Erro ao carregar logs: {e}",
        })

    # Exemplo de estatísticas simples
    top_ips = http_df['ip_address'].value_counts().head(5).reset_index()
    top_ips.columns = ['ip_address', 'count']

    top_usernames = http_df['username'].value_counts().head(5).reset_index()
    top_usernames.columns = ['username', 'count']

    return render(request, "dashboard.html", {
        "top_ips": top_ips.to_dict(orient="records"),
        "top_usernames": top_usernames.to_dict(orient="records"),
    })


# Configuração de log
base_dir = Path(__file__).resolve().parent.parent
log_path = base_dir / 'log_files' / 'http_audit.log'

funnel_logger = logging.getLogger('HTTPLogger')
funnel_logger.setLevel(logging.INFO)
if not funnel_logger.handlers:
    handler = RotatingFileHandler(log_path, maxBytes=2000, backupCount=5)
    handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
    funnel_logger.addHandler(handler)

# Credenciais do honeypot
HONEYPOT_USERNAME = "admin"
HONEYPOT_PASSWORD = "deeboodah"

# GET: renderiza a página de login
def wp_admin(request: HttpRequest) -> HttpResponse:
    return render(request, "wp-admin.html")

# POST: trata o login e registra log
@csrf_exempt
def wp_admin_login(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        ip = request.META.get('REMOTE_ADDR')

        funnel_logger.info(f', {ip}, {username}, {password}')

        if username == HONEYPOT_USERNAME and password == HONEYPOT_PASSWORD:
            return HttpResponse("Please go to https://r.mtdv.me/gYVb1JYxGw")
        else:
            return HttpResponse("Invalid username or password, please try again.")

    return redirect("wp_admin")
