# from celery import shared_task
from .update_machine_status import Command

# @shared_task
def update_machine_status_task():
    command = Command()
    command.handle()
