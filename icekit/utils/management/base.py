import time
from django.core.management.base import BaseCommand
from optparse import make_option


class CronBaseCommand(BaseCommand):
    help = ('Long running process (indefinitely) that executes task on a '
            'specified interval (default is 1 min). The intent for the '
            'management command is to be used with `django-supervisor` or '
            'similar.')

    option_list = BaseCommand.option_list + (
        make_option(
            '-i',
            '--interval',
            dest='interval',
            type='int',
            help='Number of minutes to wait before executing task.',
            default=1
        ),
    )

    def handle(self, *args, **options):
        while True:
            self.task(*args, **options)
            self.stdout.write('Sleeping for %s min.' % options['interval'])
            time.sleep(60 * options['interval'])

    def task(self, *args, **options):
        """
        The actual logic of the task to execute. Subclasses must implement
        this method.
        """
        raise NotImplementedError(
            'subclasses of CronBaseCommand must provide a task() method')
