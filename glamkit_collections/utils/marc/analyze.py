from pymarc import MARCReader
from unicode_csv import UnicodeWriter
import sys
from pprint import pprint
from tags import meaning

def _update_analysis(analysis, record_analysis, sample_length):
    # merge this record analysis into the global analysis dict

    #first create 'empty' records for all currently known tags
    for tag, stats in analysis.iteritems():
        if not record_analysis.has_key(tag):
            record_analysis[tag] = {
                'cardinality': 0,
                'samples': set(),
                'subfields': {},
            }
            for subfield in stats['subfields']:
                record_analysis[tag]['subfields'][subfield] = {
                    'cardinality': 0,
                    'samples': set(),
                }


    #now merge proper
    for tag, stats in record_analysis.iteritems():
        main_analysis = analysis.get(tag, {
            'count': 0,
            'min_cardinality': sys.maxint,
            'max_cardinality': 0,
            'subfields': {},
            'samples': set(),
        })
        main_analysis['count'] += stats['cardinality']
        main_analysis['min_cardinality'] = min(main_analysis['min_cardinality'], stats['cardinality'])
        main_analysis['max_cardinality'] = max(main_analysis['max_cardinality'], stats['cardinality'])

        if len(main_analysis['samples']) < sample_length:
            #union the two sets, then clip to the sample length - needs to be a list to do this
            main_analysis['samples'] = set(list(main_analysis['samples'].union(stats['samples']))[:sample_length])

        #and now subfields. INCEPTION
        for subfield, substats in stats['subfields'].iteritems():
            main_sub_analysis = main_analysis['subfields'].get(subfield, {
                'count': 0,
                'min_cardinality': sys.maxint,
                'max_cardinality': 0,
                'subfields': {},
                'samples': set(),
            })
            main_sub_analysis['count'] += substats['cardinality']
            main_sub_analysis['min_cardinality'] = min(main_sub_analysis['min_cardinality'], substats['cardinality'])
            main_sub_analysis['max_cardinality'] = max(main_sub_analysis['max_cardinality'], substats['cardinality'])

            if len(main_sub_analysis['samples']) < sample_length:
                #union the two sets, then clip to the sample length - needs to be a list to do this
                main_sub_analysis['samples'] = set(list(main_sub_analysis['samples'].union(substats['samples']))[:sample_length])

            main_analysis['subfields'][subfield] = main_sub_analysis

        analysis[tag] = main_analysis
    return analysis


def multifile_iter_records(files, sample_length, analysis={}):
    n = 0
    for f in files:
        if not hasattr(f, 'read'):
            f = open(f)
        reader = MARCReader(f, to_unicode=True)
        for record in reader:
            n += 1
            if n % 1000 == 0:
                sys.stderr.write("processed %s records\n" % n)
            record_analysis = {}

            fields = record.get_fields()
            for field in fields:
                attrdict = record_analysis.get(field.tag, {
                    'cardinality': 0,
                    'samples': set(),
                    'subfields': {},
                })

                attrdict['cardinality'] += 1

                if field.is_control_field():
                    if len(attrdict['samples']) < sample_length:
                        attrdict['samples'].add(field.data)
                else:
                    for subfield in field.get_subfield_tuples():
                        key =subfield[0]
                        sub_attrdict = attrdict['subfields'].get(key, {
                            'cardinality': 0,
                            'samples': set(),
                        })

                        sub_attrdict['cardinality'] += 1
                        if len(sub_attrdict['samples']) < sample_length:
                            sub_attrdict['samples'].add(subfield[1])

                        attrdict['subfields'][key] = sub_attrdict

                record_analysis[field.tag] = attrdict

            analysis = _update_analysis(analysis, record_analysis, sample_length)

    return analysis

def marcanalyze(files, sample_length=5):
    """
    returns a csv of marc keys and analyzed values, showing, for example, how many records exist.

    =================   ==============================================================
    Column              Description
    =================   ==============================================================
    ``tag``             The 3-digit MARC tag.
    ``subfield``        The single-character subfield.
    ``tag_meaning``     The English meaning of the tag/subfield, if known.
    ``record_count``    The number of records that have at least one of these tags.
    ``min_cardinality``     The minimum number of this tag or subfield that each record has.
    ``max_cardinality``     The maximum number of this tag or subfield that each record has.
    ``samples``         Non-repeating sample values of the values of each tag or subfield.
    =================   ==============================================================

    """

    analysis = multifile_iter_records(files, sample_length = sample_length)

    csv_header=("tag", "subfield", "tag_meaning", "record_count", "min_cardinality", "max_cardinality","samples")


    writer = UnicodeWriter(sys.stdout)
    writer.writerow(csv_header)

    listanalysis = [x for x in analysis.iteritems()]
    listanalysis.sort()

    for key, value in listanalysis:
        v = []
        v.append(u'"%s"' % key) #tag
        v.append(u"") # subfield
        v.append(meaning(key)) #tag_meaning
        v.append(unicode(value['count'])) #record_count
        v.append(unicode(value['min_cardinality']))
        v.append(unicode(value['max_cardinality']))
        v.append(u"\r\r".join(value['samples']))
        writer.writerow(v)

        listanalysis = [x for x in value['subfields'].iteritems()]
        listanalysis.sort()
        for subfield, value in listanalysis:
            v = []
            v.append("") #tag
            v.append(subfield) # subfield
            v.append(meaning(key, subfield)) #tag_meaning
            v.append(unicode(value['count'])) #record_count
            v.append(unicode(value['min_cardinality']))
            v.append(unicode(value['max_cardinality']))
            v.append(u"\r\r".join(value['samples']))
            writer.writerow(v)

