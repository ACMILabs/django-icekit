#!/usr/bin/env python
# −*− coding: UTF−8 −*−

from optparse import make_option
from django.core.management import BaseCommand
from glamkit_collections.utils.files import getfiles


class AnalysisCommand(BaseCommand):
    help = "Prints a csv-formatted analysis of paths for all files found at the given paths."
    file_regex = r"\.xml$"

    option_list = BaseCommand.option_list + (
        make_option('-r', '--recursive',
            action='store_true',
            dest='recursive',
            default=False,
            help="traverse the given folder recursively"
        ),
        make_option("-l", "--list",
            action="store_true",
            dest="list_only",
            default=False,
            help="only list the files that would be analyzed"
        ),
        make_option("-s", "--samplesize",
            action="store",
            dest="sample_length",
            default=5,
            help="provide this many samples of each element's text (default: 5)"
        ),
    )

    def analyze(self, paths, sample_length):
        raise NotImplementedError

    def handle(self, *args, **options):
        try:
            path = args[0]
        except IndexError:
            path = "./"

        paths = getfiles(path=path, regex=self.file_regex, recursive=options['recursive'])

        if options['list_only']:
            for p in paths:
                print p
        else:
            self.analyze(paths, sample_length=options['sample_length'])
