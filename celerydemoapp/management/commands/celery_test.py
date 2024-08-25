from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("action", type=str)
        parser.add_argument("arg1", nargs="?", type=str)
        parser.add_argument("arg2", nargs="?", type=str)
        parser.add_argument("arg3", nargs="?", type=str)
        parser.add_argument("arg4", nargs="?", type=str)

    def handle(self, *args, **options):
        action = getattr(self, options["action"], None)
        action(options)

    def basic(self, options):
        from celerydemoapp.tasks import add

        result = add.delay(4, 6)  # Call the Celery task asynchronously
        print(f"Task ID: {result.id}")
        print(f"Result: {result.get(timeout=10)}")

        for i in range(1, 10):
            result = add.delay(i, 6)  # Call the Celery task asynchronously
            print(f"Task ID: {result.id}")
        print(f"Result: {result.get(timeout=1000)}")

    def email(self, options):
        print("send email")
        from celerydemoapp.mytasks.order_tasks import send_email_task

        for i in range(1, 3):
            send_email_task.delay("arunss@yopmail.com", "Testing Email", "Hellow")
