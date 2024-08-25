from django.core.management.base import BaseCommand, CommandError
from django.db import connections
from django.db.utils import OperationalError
from django.conf import settings
import redis
import requests
import os


class Command(BaseCommand):
    help = "Runs various tests to check system health and configurations."

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Starting system tests..."))

        # self.check_database()
        self.check_redis()
        self.check_external_api()
        # self.print_environment_variables()

        self.stdout.write(self.style.SUCCESS("All tests completed successfully."))

    def check_database(self):
        self.stdout.write("Checking database connectivity...")
        try:
            db_conn = connections["default"]
            db_conn.cursor()
            self.stdout.write(self.style.SUCCESS("Database connection successful."))
        except OperationalError as e:
            raise CommandError(f"Database connection failed: {e}")

    def check_redis(self):
        self.stdout.write("Checking Redis connectivity...")
        try:
            redis_url = (
                settings.REDIS_URL
                if hasattr(settings, "REDIS_URL")
                else "redis://localhost:6379/0"
            )
            client = redis.StrictRedis.from_url(redis_url)
            client.ping()
            self.stdout.write(self.style.SUCCESS("Redis connection successful."))
        except redis.exceptions.ConnectionError as e:
            raise CommandError(f"Redis connection failed: {e}")

    def check_external_api(self):
        self.stdout.write("Checking external API connectivity...")
        try:
            response = requests.get("https://api.github.com")
            if response.status_code == 200:
                self.stdout.write(self.style.SUCCESS("External API is reachable."))
            else:
                raise CommandError(
                    f"External API returned unexpected status code: {response.status_code}"
                )
        except requests.exceptions.RequestException as e:
            raise CommandError(f"External API connection failed: {e}")

    def print_environment_variables(self):
        self.stdout.write("Printing important environment variables...")
        env_vars = ["DEBUG", "SECRET_KEY", "DATABASE_URL", "REDIS_URL"]
        for var in env_vars:
            value = os.getenv(var, "Not Set")
            self.stdout.write(f"{var}: {value}")
