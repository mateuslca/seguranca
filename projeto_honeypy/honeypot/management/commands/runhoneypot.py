from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from honeypot.ssh_honeypot import honeypot

class Command(BaseCommand):
    help = 'Executa o honeypot SSH ou HTTP'

    def add_arguments(self, parser):
        parser.add_argument('-a', '--address', type=str, required=True)
        parser.add_argument('-p', '--port', type=int, required=True)
        parser.add_argument('-u', '--username', type=str, default="admin")
        parser.add_argument('-w', '--password', type=str, default="deeboodah")
        parser.add_argument('--ssh', action='store_true', help='Executa o honeypot SSH')
        parser.add_argument('--http', action='store_true', help='Executa o honeypot HTTP com servidor Django embutido')
        parser.add_argument('--tarpit', action='store_true', help='Ativa o tarpit para SSH')

    def handle(self, *args, **options):
        if options['ssh']:
            self.stdout.write(self.style.NOTICE("[-] Executando honeypot SSH..."))
            honeypot(
                address=options['address'],
                port=options['port'],
                username=options['username'],
                password=options['password'],
                tarpit=options['tarpit']
            )

        elif options['http']:
            address = options['address']
            port = options['port']
            self.stdout.write(self.style.NOTICE(f"[-] Iniciando honeypot HTTP via Django em http://{address}:{port}/wp-admin"))

            # Chama internamente o runserver com host e porta
            call_command('runserver', f'{address}:{port}')

        else:
            raise CommandError("Você deve escolher entre --ssh ou --http")
