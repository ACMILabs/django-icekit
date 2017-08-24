#!/usr/bin/env python
# −*− coding: UTF−8 −*−

from glamkit_collections.utils.xml.lib.analyze import xmlanalyze
from . import AnalysisCommand


class Command(AnalysisCommand):
    help = "Prints a csv-formatted analysis of paths for all MARC files found at the given paths."
    file_regex = r"\.xml$"

    def analyze(self, paths, sample_length):
        return xmlanalyze(paths, sample_length)

