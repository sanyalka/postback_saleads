from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create or update a development superuser.'

    def add_arguments(self, parser):
        parser.add_argument('--username', default='admin')
        parser.add_argument('--password', default='admin')
        parser.add_argument('--email', default='admin@example.com')

    def handle(self, *args, **options):
        User = get_user_model()
        user, _ = User.objects.update_or_create(
            username=options['username'],
            defaults={'email': options['email'], 'is_staff': True, 'is_superuser': True},
        )
        user.set_password(options['password'])
        user.save()
        self.stdout.write(self.style.SUCCESS(f"Admin user '{user.username}' is ready"))
