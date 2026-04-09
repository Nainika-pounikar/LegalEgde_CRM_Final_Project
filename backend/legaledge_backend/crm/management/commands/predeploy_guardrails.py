from django.conf import settings
from django.core.management import BaseCommand, CommandError, call_command
from django.db import DEFAULT_DB_ALIAS, connections
from django.db.migrations.executor import MigrationExecutor
from django.db.utils import OperationalError


class Command(BaseCommand):
    help = 'Run strict production pre-deployment checks and fail on any unsafe configuration.'

    def handle(self, *args, **options):
        if settings.DEBUG:
            raise CommandError(
                'DJANGO_DEBUG is True. Run this command with DJANGO_DEBUG=False to simulate production.'
            )

        self.stdout.write('1/5 Running django deploy checks...')
        call_command('check', '--deploy')

        self.stdout.write('2/5 Verifying database connection...')
        try:
            connections[DEFAULT_DB_ALIAS].ensure_connection()
        except OperationalError as exc:
            raise CommandError(
                'Database connection failed. Verify DATABASE_URL/DB_SSLMODE and connectivity.'
            ) from exc

        self.stdout.write('3/5 Verifying no pending migrations...')
        executor = MigrationExecutor(connections[DEFAULT_DB_ALIAS])
        plan = executor.migration_plan(executor.loader.graph.leaf_nodes())
        if plan:
            pending = [f'{migration.app_label}.{migration.name}' for migration, _ in plan]
            raise CommandError(
                'Pending migrations detected. Run "python manage.py migrate --noinput". '
                f'Pending: {", ".join(pending)}'
            )

        self.stdout.write('4/5 Running migrate --noinput (idempotent safety)...')
        call_command('migrate', '--noinput')

        self.stdout.write('5/5 Running collectstatic --noinput...')
        call_command('collectstatic', '--noinput')

        self.stdout.write(self.style.SUCCESS('Pre-deployment guardrails passed.'))
