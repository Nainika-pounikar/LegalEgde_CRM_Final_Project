import logging
import os
from pathlib import Path

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import DEFAULT_DB_ALIAS, connections
from django.db.migrations.executor import MigrationExecutor
from django.db.utils import OperationalError, ProgrammingError


logger = logging.getLogger(__name__)


def _require_env_vars(names):
    missing = [name for name in names if not os.environ.get(name, '').strip()]
    if missing:
        raise ImproperlyConfigured(
            f'Missing required environment variables: {", ".join(sorted(missing))}.'
        )


def _validate_database_connection():
    try:
        connections[DEFAULT_DB_ALIAS].ensure_connection()
    except OperationalError as exc:
        raise ImproperlyConfigured(
            'Database is unreachable. Verify DATABASE_URL, DB credentials, network, and DB_SSLMODE.'
        ) from exc


def _validate_no_pending_migrations():
    connection = connections[DEFAULT_DB_ALIAS]
    try:
        executor = MigrationExecutor(connection)
    except (OperationalError, ProgrammingError) as exc:
        raise ImproperlyConfigured(
            'Unable to inspect migrations. Ensure database is initialized and reachable.'
        ) from exc

    plan = executor.migration_plan(executor.loader.graph.leaf_nodes())
    if plan:
        pending = [f'{migration.app_label}.{migration.name}' for migration, _ in plan]
        raise ImproperlyConfigured(
            'Pending migrations detected. Run "python manage.py migrate --noinput" before startup. '
            f'Pending: {", ".join(pending)}'
        )


def _validate_static_artifacts():
    static_root = Path(settings.STATIC_ROOT)
    if not static_root.exists() or not static_root.is_dir():
        raise ImproperlyConfigured(
            f'STATIC_ROOT "{static_root}" is missing. Run "python manage.py collectstatic --noinput".'
        )

    manifest_path = static_root / 'staticfiles.json'
    if not manifest_path.exists():
        raise ImproperlyConfigured(
            f'Static manifest "{manifest_path}" is missing. Run collectstatic before deployment.'
        )


def run_startup_guards():
    """
    Production startup guardrails.
    Intended to run from WSGI startup so deploys fail fast.
    """
    if settings.DEBUG:
        return

    _require_env_vars(
        [
            'SECRET_KEY',
            'DATABASE_URL',
            'DB_SSLMODE',
            'FRONTEND_URL',
            'ALLOWED_HOSTS',
            'CORS_ALLOWED_ORIGINS',
            'CSRF_TRUSTED_ORIGINS',
        ]
    )

    if os.environ.get('DB_SSLMODE', '').strip().lower() != 'require':
        raise ImproperlyConfigured('DB_SSLMODE must be "require" in production.')

    _validate_database_connection()
    _validate_no_pending_migrations()
    _validate_static_artifacts()
    logger.info('Production startup guards passed.')

