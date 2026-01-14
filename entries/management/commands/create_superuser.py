"""
Management command to create a superuser automatically.
This is useful for deployment environments like Railway.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

User = get_user_model()


class Command(BaseCommand):
    help = 'Creates a superuser from environment variables if it does not exist'

    def handle(self, *args, **options):
        username = os.environ.get('SUPERUSER_USERNAME', 'deanna')
        email = os.environ.get('SUPERUSER_EMAIL', 'deanna.riddlespur@gmail.com')
        password = os.environ.get('SUPERUSER_PASSWORD', 'Sunshine101!')

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'Superuser "{username}" already exists. Skipping creation.')
            )
            return

        if User.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.WARNING(f'User with email "{email}" already exists. Skipping creation.')
            )
            return

        try:
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created superuser "{username}"')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating superuser: {str(e)}')
            )

