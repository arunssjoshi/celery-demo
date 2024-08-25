from celery import shared_task
import time
from datetime import datetime


@shared_task
def add(x, y):
    time.sleep(5)
    return x + y


@shared_task
def my_periodic_task():
    print("This task runs every 20 seconds")


@shared_task
def send_daily_report():
    # Task to send a daily report
    print(f"Daily report sent at {datetime.now()}")


@shared_task
def run_payment_settlement():
    # Task to send a daily report
    print(f"run_payment_settlement at {datetime.now()}")
