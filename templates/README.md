# Templates

Every page extends `base.html` (sidebar, header, messages, footer). Templates are grouped by module.

| Folder | Templates | Purpose |
|---|---|---|
| (root) | `base.html` | Master layout: sidebar by role, header, search, notifications |
| `errors/` | `403.html`, `404.html`, `500.html` | Permission denied, not found, server error |
| `shared/` | `generic_form.html`, `_form_card.html`, `_field.html`, `_empty.html`, `_pagination.html` | Reusable form page and small partials |
| `accounts/` | `auth_base.html`, `login.html`, `simple_form.html`, `profile.html`, `user_list.html`, `password_reset_email.txt` | Sign-in, password reset, profile, user management |
| `dashboard/` | `index.html`, `search.html` | Role-based dashboard and global search |
| `projects/` | `list.html`, `form.html`, `detail.html`, `review.html` | Register, view and approve projects |
| `monitoring/` | `dashboard.html`, `update_list.html`, `form.html`, `review.html` | Visits, progress updates and verification |
| `results/` | `list.html` | Results framework indicators |
| `beneficiaries/` | `dashboard.html`, `list.html`, `form.html`, `detail.html` | Beneficiary records |
| `finance/` | `dashboard.html`, `list.html` | Payments |
| `grm/` | `dashboard.html`, `list.html`, `detail.html` | Grievance cases |
| `documents/` | `list.html` | Documents and evidence |
| `reports/` | `index.html`, `filter.html`, `result.html`, `quality.html` | Reports, export and data quality |
| `notifications/` | `list.html` | In-system notifications |
| `audit/` | `list.html` | Audit trail |
