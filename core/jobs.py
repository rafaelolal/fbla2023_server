"""Source: https://stackoverflow.com/questions/44896618/django-run-a-function-every-x-seconds/44897678
Runs the "archive" command from the django_archives
app every day at midnight to dynamically backup the database
django_archives: https://django-archive.readthedocs.io/en/latest/
"""

from schedule import Scheduler
import threading
import time

from django.core.management import call_command


def run_continuously(self, interval: int = 1) -> threading.Event:
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):

        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                self.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.setDaemon(True)
    continuous_thread.start()

    return cease_continuous_run


Scheduler.run_continuously = run_continuously


def start_scheduler() -> None:
    scheduler = Scheduler()
    scheduler.every().day.at("00:00").do(call_archive)
    scheduler.run_continuously()


def call_archive() -> None:
    call_command('archive')
