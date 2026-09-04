from io import StringIO

from django.core.management import call_command
from django.test import TestCase, override_settings


class PendingMigrationsTests(TestCase):
    def test_no_pending_migrations(self):
        out = StringIO()
        try:
            call_command(
                "makemigrations",
                "--dry-run",
                "--check",
                stdout=out,
                stderr=StringIO(),
            )
        except SystemExit:  # pragma: no cover
            raise AssertionError("Pending migrations:\n" + out.getvalue()) from None


class HealthCheckTestCase(TestCase):
    @override_settings(
        CACHES={"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}
    )
    def test_health_check_is_public_and_checks_dependencies(self):
        response = self.client.get("/healthz")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cache(alias=")
        self.assertContains(response, "Database(alias=")
