"""First-run setup: make sure the nine roles exist and create the first administrator.

    python manage.py setup_system                      # asks for the details
    python manage.py setup_system --username issa --email you@example.org   # asks only for the password

After this, sign in and create every other user from  Users > Add user  (administrator only).
"""
import getpass

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError

from accounts.apps import create_roles
from accounts.models import Role


class Command(BaseCommand):
    help = "Create the system roles and the first administrator account."

    def add_arguments(self, parser):
        parser.add_argument("--username")
        parser.add_argument("--email")
        parser.add_argument("--first-name", default="")
        parser.add_argument("--last-name", default="")
        parser.add_argument("--password", help="Avoid on shared machines; you will be asked if omitted.")

    def handle(self, *args, **o):
        User = get_user_model()
        create_roles(None)
        self.stdout.write(f"Roles ready: {Role.objects.count()}")
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(self.style.WARNING("An administrator already exists; nothing more to do."))
            return
        username = o["username"] or input("Administrator username: ").strip()
        email = o["email"] or input("Email address: ").strip()
        first = o["first_name"] or input("First name: ").strip()
        last = o["last_name"] or input("Last name: ").strip()
        if not username:
            raise CommandError("A username is required.")
        pw = o["password"]
        while not pw:
            a, b = getpass.getpass("Password: "), getpass.getpass("Password (again): ")
            if a != b:
                self.stderr.write("Passwords do not match.")
                continue
            try:
                validate_password(a)
            except ValidationError as e:
                self.stderr.write("\n".join(e.messages))
                continue
            pw = a
        u = User.objects.create_superuser(username=username, email=email, password=pw, first_name=first, last_name=last)
        u.role = Role.objects.get(name="administrator")
        u.save(update_fields=["role"])
        self.stdout.write(self.style.SUCCESS(f"Administrator '{username}' created. Start the server and sign in."))
