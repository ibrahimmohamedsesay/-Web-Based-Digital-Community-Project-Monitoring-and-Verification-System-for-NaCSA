"""Create one ready-to-use account for each of the nine roles (for testing, training and the project defence).

    python manage.py create_accounts

Existing usernames are skipped unless --reset is given, which sets the password listed here. Change these passwords before any real use.
"""
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from accounts.apps import create_roles
from accounts.models import Role

ACCOUNTS = [
    ("admin", "administrator", "System", "Administrator", "Admin@NaCSA2026"),
    ("management", "management", "Management", "User", "Mgmt@NaCSA2026"),
    ("me_officer", "me_officer", "M&E", "Officer", "MandE@NaCSA2026"),
    ("project_manager", "project_manager", "Project", "Manager", "ProjMgr@NaCSA2026"),
    ("field_officer", "field_officer", "Field", "Officer", "Field@NaCSA2026"),
    ("finance_officer", "finance_officer", "Finance", "Officer", "Finance@NaCSA2026"),
    ("grm_officer", "grm_officer", "GRM", "Officer", "Grm@NaCSA2026"),
    ("data_entry", "data_entry_officer", "Data Entry", "Officer", "DataEntry@NaCSA2026"),
    ("viewer", "viewer", "Viewer", "User", "Viewer@NaCSA2026"),
]


class Command(BaseCommand):
    help = "Create one account for each of the nine roles."

    def add_arguments(self, parser):
        parser.add_argument("--reset", action="store_true", help="Also reset the password and role of accounts that already exist.")

    def handle(self, *args, **o):
        User = get_user_model()
        create_roles(None)
        for username, role, first, last, pw in ACCOUNTS:
            existing = User.objects.filter(username=username).first()
            if existing:
                if o["reset"]:
                    existing.set_password(pw)
                    existing.role = Role.objects.get(name=role)
                    existing.is_active = True
                    if role == "administrator":
                        existing.is_staff = existing.is_superuser = True
                    existing.save()
                    self.stdout.write(self.style.SUCCESS(f"reset: {username}"))
                else:
                    self.stdout.write(f"skipped (exists): {username}  (use --reset to set the password above)")
                continue
            u = User.objects.create_user(username=username, password=pw, first_name=first, last_name=last,
                                         email=f"{username}@example.org")
            u.role = Role.objects.get(name=role)
            if role == "administrator":
                u.is_staff = u.is_superuser = True
            u.save()
            self.stdout.write(self.style.SUCCESS(f"created: {username} ({role})"))
