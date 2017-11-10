from pprint import pprint
import sys
import csv

from icekit.utils.csv_unicode import UnicodeWriter

csv_header=("path", "min_cardinality", "max_cardinality","samples", "attributes")
from iterxml import multifile_iter_elems
from utils import remove_ns, get_path

def _get_children_from_analysis(path, analysis):
    keys = analysis.keys()
    for k in keys:
        if k.startswith(path) and k != path: # k is a decendent, but not necessarily a child.
            if len(k[len(path):].split('.')) == 2: #it's a child ['', 'child']
                yield k


def analyze_start(elem, analysis, sample_length):
    path = get_path(elem)

    if not analysis.has_key(path):
        analysis[path] = {
            'cardinality_current': 0,
            'cardinality_min': sys.maxint,
            'cardinality_max': 0,
            'values': set(),
            'attributes': {},
        }

    analysis[path]['cardinality_current'] += 1
    #maintain max
    if analysis[path]['cardinality_current'] > analysis[path]['cardinality_max']:
        analysis[path]['cardinality_max'] = analysis[path]['cardinality_current']

    #attributes
    for attr in elem.keys():
        av = analysis[path]['attributes'].get(attr, set())
        if len(av) < sample_length:
            av.add(elem.get(attr))
            analysis[path]['attributes'][attr] = av


def analyze_end(elem, analysis, sample_length):
    path = get_path(elem)

    # maintain min
    for c in _get_children_from_analysis(path, analysis):
        if analysis[c]['cardinality_current'] < analysis[c]['cardinality_min']:
            analysis[c]['cardinality_min'] = analysis[c]['cardinality_current']
        analysis[c]['cardinality_current'] = 0
    # sample values
    if len(analysis[path]['values']) < sample_length:
        try:
            v = elem.text.strip()
            if v:
                analysis[path]['values'].add(v)
        except AttributeError:
            pass

def _attributestring(attrdict):
    ss = []
    for key, value in attrdict.iteritems():
        s = "%s = (\"%s\")" % (remove_ns(key), "\", \"".join(value))
        ss.append(s)

    return "\r\n\r\n".join(ss)

def xmlanalyze(files, sample_length=5):
    """ returns a csv of xml paths and analyzed values, showing, for example, how many records exist for every path in an xml file """

    # data structure to store results
    analysis = {}

    multifile_iter_elems(files, analyze_start, analyze_end, sample_length=sample_length, analysis=analysis)

    writer = UnicodeWriter(sys.stdout)
    writer.writerow(csv_header)

    listanalysis = [x for x in analysis.iteritems()]
    listanalysis.sort()

    for key, value in listanalysis:
        v = []
        v.append(key) #path
        if value['cardinality_min'] == sys.maxint: #top-level nodes do this.
            value['cardinality_min'] = value['cardinality_max']
        v.append(value['cardinality_min'])
        v.append(value['cardinality_max'])
        v.append("\r\r".join(value['values']))
        v.append(_attributestring(value['attributes']))

        writer.writerow(v)
