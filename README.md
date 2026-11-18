# NaCSA Community Project Monitoring & Verification System

*Design and Evaluation of a Web-Based Digital Community Project Monitoring and Verification System for the National Commission for Social Action (NaCSA), Sierra Leone.*
Authors: Issa Kamara, Khadijah Kubra Bunduka, Ibrahim Mohamed Sesay — Limkokwing University of Creative Technology.

The system starts **empty**. You create the first administrator, then the administrator creates every other user, and real projects and records are entered through the screens.

## Stack
Django 5.2 · PostgreSQL · Django REST Framework (read-only API) · vanilla JS + Chart.js (vendored, works offline) · ReportLab / openpyxl for PDF / Excel.

## Modules
Dashboard · Projects (lifecycle, 6-step registration, approval workflow) · Monitoring & M&E (progress updates with photo evidence, verification review, visits, evaluations) · Results framework · Beneficiaries · Finance & payments · Grievance redress (GRM) · Documents & evidence (restricted downloads) · Reports (12 types; print / PDF / Excel / CSV; data-quality checks) · Notifications · Audit trail · User management.

## Install (Windows / VS Code)
1. Install Python 3.11+ and PostgreSQL 14+. Create the database: `CREATE DATABASE nacsa_db;`
2. In the project folder:
```
python -m venv venv
venv\Scripts\activate            (macOS/Linux: source venv/bin/activate)
pip install -r requirements.txt
copy .env.example .env           (then edit SECRET_KEY, DB_PASSWORD)
python manage.py migrate
python manage.py setup_system    (creates the roles and the first administrator; asks for a password)
python manage.py runserver
```
3. Open http://127.0.0.1:8000/ and sign in with the administrator you just created.

## First steps after sign-in
1. **Users → Add user**: create one account per staff member and give each a role.
2. **Projects → Register project**: enter a real project and submit it for approval.
3. A *different* Project Manager approves it (nobody can approve a project they registered).
4. Field officers submit progress updates with photos; an M&E officer verifies them. Official progress changes only after verification.
5. Record beneficiaries, payments, grievances and documents as work proceeds; run reports from **Reports & analytics**.

## Roles
Administrator · Management · M&E Officer · Project Manager · Field Officer · Finance Officer · GRM Officer · Data Entry Officer · Viewer. The permission table is in one file: `core/permissions.py`.

## Tests
`python manage.py test` — 44 automated tests (sign-in and lockout, role permissions, approval workflow, verification, beneficiaries, payments, GRM, document access, reports and exports, notifications, audit, XSS, CSRF, API roles).

## Going live (production checklist)
- `.env`: `DEBUG=False`, a long random `SECRET_KEY`, `ALLOWED_HOSTS=your.domain`, strong `DB_PASSWORD`.
- Serve over HTTPS (set `SECURE_SSL_REDIRECT=True`); run `python manage.py collectstatic`.
- Configure email (`EMAIL_BACKEND` and SMTP settings) so password-reset and notification emails are delivered; until then reset links print in the server console.
- Serve uploaded evidence photos through the web server (with `DEBUG=False` Django no longer serves them); keep the `media/documents/` folder private, since documents are released only through the permission-checked download page.
- Back up the PostgreSQL database and the `media/` folder regularly.

## Security
Role check on every page and API call · CSRF on all forms · sign-in lockout after 5 failures for 10 minutes · safe redirects · upload type and size limits · restricted documents only via a permission-checked download · CSV/Excel formula-injection guard · read-only audit trail · secrets in `.env`.

## Known limits
No SMS; email only once configured. No offline data capture. No map view. English only.
