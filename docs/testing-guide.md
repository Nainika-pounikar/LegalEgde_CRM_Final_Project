# Testing Guide

This guide validates the restructured monorepo setup and core CRM flows.

## Prerequisites

- Backend running from `backend/` on `http://127.0.0.1:8000`
- Frontend running from `frontend/` on `http://127.0.0.1:5173`
- Seed data loaded (`python manage.py seed_data`)

## Automated Checks

Run from repository root:

```bash
python backend/manage.py check
python backend/manage.py migrate --plan
```

Run from `frontend/`:

```bash
npm install
npm run lint
npm test
npm run build
```

Expected result:
- Django reports no system-check issues
- No pending migrations (or clearly listed planned operations)
- Frontend lint passes
- All Vitest specs pass
- Vite build succeeds

## Manual Smoke Tests

1. Authentication
- Log in with seeded admin/manager/user accounts.
- Verify role-appropriate dashboard loads.

2. CRM CRUD
- Create, update, and delete a Contact and Task.
- Refresh the page and confirm persisted data remains correct.

3. Calls and Meetings
- Open Calls page.
- Start a call from the "Call Again" action.
- Toggle Hold/Resume and confirm toast feedback is shown.
- Schedule a meeting and verify it appears in Upcoming Meetings.

4. Inbox and Notifications
- Open Inbox list and thread views.
- Mark at least one message read.
- Verify unread notification count updates.

5. Dashboard APIs
- Validate these endpoints in browser or Postman:
  - `GET /api/dashboard/admin/`
  - `GET /api/dashboard/manager/`
  - `GET /api/dashboard/user/`
  - `GET /api/dashboard/recent-activity/`

## Regression Checklist

- [ ] No hardcoded credentials in tracked files
- [ ] `.env` files remain untracked
- [ ] No `node_modules`, `venv`, `dist`, `build`, `__pycache__`, or log files committed
- [ ] Frontend API calls target `VITE_API_BASE_URL`
- [ ] Backend CORS/CSRF origins match frontend URL
