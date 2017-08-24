#!/usr/bin/env python
# −*− coding: UTF−8 −*−

from . import AnalysisCommand
from glamkit_collections.utils.marc.analyze import marcanalyze


class Command(AnalysisCommand):
    help = "Prints a csv-formatted analysis of paths for all XML files found at the given paths."
    file_regex = r"\.mrc$"

    def analyze(self, paths, sample_length):
        return marcanalyze(paths, sample_length)

