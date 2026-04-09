# LegalEdge CRM

LegalEdge CRM is a full-stack customer relationship platform for legal and service teams. It combines lead/deal management, team dashboards, email workflows, marketing modules, and role-based access in a production-ready monorepo.

## Features

- Role-based authentication (`admin`, `manager`, `user`) with JWT access/refresh tokens
- CRM workflows for contacts, leads, deals, tasks, calls, meetings, tickets, and notes
- Dashboard APIs for admin, manager, and individual contributors
- Email send + inbox sync flows (OAuth providers + SMTP fallback)
- Marketing modules (campaigns, ads, forms, events, social, buyer intent, lead scoring)
- Frontend test/lint/build pipeline with Vite + Vitest + ESLint
- Environment-first backend configuration for secure local and production deployment

## Tech Stack

- Backend: Django, Django REST Framework, Simple JWT, django-cors-headers, WhiteNoise
- Frontend: React 18, React Router, Vite, Vitest, ESLint, Prettier
- Database: SQLite (local), PostgreSQL (production via `DATABASE_URL`)
- Deployment-ready components: Gunicorn, WhiteNoise, environment-based security settings

## Repository Structure

```text
LegalEdge-CRM/
|-- backend/
|   |-- legaledge_backend/
|   |   |-- accounts/
|   |   |-- crm/
|   |   `-- config/
|   |-- manage.py
|   |-- requirements.txt
|   `-- .env.example
|-- frontend/
|   |-- src/
|   |-- public/
|   |-- package.json
|   |-- vite.config.js
|   `-- .env.example
|-- docs/
|   `-- testing-guide.md
|-- .env.example
|-- .gitignore
`-- README.md
```

## Architecture

- `frontend/`: SPA UI, routing, dashboards, CRUD interfaces, API client, local UX state
- `backend/legaledge_backend/accounts`: auth, profile, password management
- `backend/legaledge_backend/crm`: CRM models, dashboards, notifications, inbox, email integrations
- `backend/legaledge_backend/config`: settings, middleware, URL routing, deployment guardrails

## Quick Start

## 1) Prerequisites

- Python 3.11+
- Node.js 20+
- npm 10+

## 2) Backend Setup

```bash
cd backend
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies and configure environment:

```bash
pip install -r requirements.txt
```

```bash
cp .env.example .env
```

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Run database setup:

```bash
python manage.py migrate
python manage.py seed_data
```

Start backend:

```bash
python manage.py runserver
```

Backend URL: `http://127.0.0.1:8000`

## 3) Frontend Setup

Open a new terminal:

```bash
cd frontend
npm install
```

```bash
cp .env.example .env
```

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Start frontend:

```bash
npm start
```

Frontend URL: `http://127.0.0.1:5173`

## Run From Repository Root (Optional)

You can also run frontend commands from the repo root now:

```bash
npm run install:frontend
npm run dev
```

## Environment Variables

### Backend (`backend/.env`)

| Variable | Purpose |
| --- | --- |
| `SECRET_KEY` | Django secret key (required) |
| `DJANGO_DEBUG` | Local debug toggle |
| `ALLOWED_HOSTS` | Allowed hostnames for Django |
| `DATABASE_URL` | Production PostgreSQL connection string |
| `DB_ENGINE` | Local fallback engine (`sqlite` or `postgres`) |
| `FRONTEND_URL` | Frontend origin used in CORS/CSRF settings |
| `EMAIL_HOST_USER` / `EMAIL_HOST_PASSWORD` | SMTP sender credentials |

### Frontend (`frontend/.env`)

| Variable | Purpose |
| --- | --- |
| `VITE_API_BASE_URL` | API base URL (`/api` for local proxy) |
| `VITE_SHOW_AUTH_DEBUG` | Auth debug panel toggle |
| `VITE_ENABLE_NOTIF_WS` | Notification websocket toggle |
| `VITE_ENABLE_OFFLINE_LOGIN` | Offline login fallback toggle |

## API Endpoints (Core)

### Auth

- `POST /api/auth/login/`
- `POST /api/auth/signup/`
- `GET/PATCH /api/auth/me/`
- `POST /api/auth/refresh/`
- `POST /api/auth/change-password/`

### CRM

- `/api/contacts/`, `/api/leads/`, `/api/deals/`, `/api/tasks/`, `/api/companies/`, `/api/tickets/`
- `/api/calls/`, `/api/meetings/`, `/api/activities/`, `/api/notes/`

### Dashboards / Ops

- `GET /api/dashboard/admin/`
- `GET /api/dashboard/manager/`
- `GET /api/dashboard/user/`
- `GET /api/dashboard/recent-activity/`

### Communication

- `POST /api/email/send/`
- `GET /api/inbox/`
- `GET /api/notifications/`

## Screenshots

Add screenshots to `docs/screenshots/` and replace placeholders below:

- `![Dashboard](docs/screenshots/dashboard.png)`
- `![Contacts](docs/screenshots/contacts.png)`
- `![Deals](docs/screenshots/deals.png)`

## Code Quality

- Structured monorepo separation (`backend/` and `frontend/`)
- Environment-safe defaults with `.env.example` templates
- Source-controlled cleanup (`node_modules`, `venv`, logs, build outputs ignored)
- Frontend lint/test/build scripts verified after restructuring
- Backend system checks and migration checks verified after restructuring

## Future Enhancements

- Add CI workflows for backend + frontend checks on every PR
- Add API schema docs (OpenAPI/Swagger)
- Add Docker Compose for one-command local startup
- Expand unit/integration coverage for backend business rules

## Author

Nainika Pounikar

For collaboration or hiring discussions, use the GitHub profile linked with this repository.
