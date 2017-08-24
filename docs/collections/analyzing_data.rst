GLAMkit comes with tools for analysing and harvesting from large collections of various file types, currently:

   * JSON files
   * XML files with unwieldy or undefined schemas (which may also be badly-formed)
   * MARC files which use an undocumented set of fields (which may also be badly-formed)

Requirements
------------
The different data formats (except for JSON) use libraries that may not be installed by default. Alter the optional
``import_*`` extras in your project's ``requirements-icekit.txt`` to install them, like this::

   -e git+https://github.com/ic-labs/django-icekit@develop#egg=django-icekit[ ... ,import_xml]


JSON Analysis
=============

*(to be documented)*

XML Analysis
============

(Add ``import_xml`` to ``requirements-icekit.txt`` to install dependencies)

``manage.py analyze_xml`` is a command-line tool that takes a path (or ``./``) and returns a csv file containing an
analysis of every element in every xml file in the path. It requires the ``lxml`` library.

Usage examples::

    manage.py analyze_xml --help               # show help
    manage.py analyze_xml -l                   # list all xml files to be analyzed
    manage.py analyze_xml                      # analyze all xml files in the current path
    manage.py analyze_xml > analysis.csv       # analyze all xml files in the current path and write the results to a csv file.
    manage.py analyze_xml path/to/xml/         # analyze all xml files in the given path
    manage.py analyze_xml path/to/file.xml     # analyze a single xml file
    manage.py analyze_xml path/to/xml/ -r      # traverse the current path recursively

The analysis csv contains these fields:

=================    ==============================================================
Column               Description
=================    ==============================================================
``path``             A dot-separated path to each XML tag.
``min_cardinality``  The minimum number of these elements that each of its parents has.
``max_cardinality``  The maximum number of these elements that each of its parents has.
``samples``          Non-repeating sample values of the text within the XML tag.
``attributes``       A list of all the attributes found for each tag.
=================    ==============================================================


Interpreting the analysis
-------------------------

path
~~~~

The path is dot-separated. A path that ``looks.like.this`` represents the <this> tag of a file structured like this::

   <looks>
      <like>
         <this></this>
      </like>
   </looks>

min/max_cardinality
~~~~~~~~~~~~~~~~~~~

``min_cardinality`` and ``max_cardinality`` will tell you the minimum and maximum number of these elements you'll have
to deal with each time you encounter them. If a ``min_cardinality`` is 0, it means the element is optional. If a
``max_cardinality`` is 1 it means that it's a singleton value. If ``max_cardinality`` is more than 1, it means that the
element is repeated to make up a list.

samples
~~~~~~~

``samples`` is a particularly useful field. Apart from seeing the values to discern their likely data type, you can
see the variety of values produced.

Set the number of samples to track with the ``--samplesize`` option. The default value is 5.

If you asked for 5 sample values, but only got 1 value, that means the value is constant. If you get 2 values, that
means there are only 2 values in the entire collection (which means that the value could be boolean). If you got 0
values, that means the tag is always empty, or only ever contains children (see the next row of the csv file to see
if an element has any children).

The number of sample values can be set with the ``-n`` option to ``analyze_xml``, but you should keep it more than 3
for easily discerning the range of values.

attributes
~~~~~~~~~~

This field lists out all the attributes found for the tag, and a sample of their values.

MARC Analysis
=============

(Add ``import_marc`` to ``requirements-icekit.txt`` to install dependencies)


``manage.py analyze_marc`` is a command-line tool that takes a path (or ``./``) and returns a csv file containing an
analysis of every MARC file found in the path.  It requires the ``pymarc`` library.

Usage examples::

    manage.py analyze_marc --help              # show help
    manage.py analyze_marc -l                  # list all marc files to be analyzed
    manage.py analyze_marc                     # analyze all MARC files in the current path
    manage.py analyze_marc > analysis.csv      # analyze all MARC files in the current path and write the results to a csv file.
    manage.py analyze_marc path/to/marc/       # analyze all MARC files in the given path
    manage.py analyze_marc path/to/file.mrc    # analyze a single MARC file
    manage.py analyze_marc path/to/marc/ -r    # traverse the current path recursively

The analysis csv has a row for each tag (with an empty subfield column), and a row for each subfield. Each row contains
these fields:

=================    ==============================================================
Column               Description
=================    ==============================================================
``tag``              The 3-digit MARC tag.
``subfield``         The single-character subfield.
``tag_meaning``      The English meaning of the tag/subfield, if known.
``record_count``     The number of records that have at least one of these tags.
``min_cardinality``  The minimum number of this tag or subfield that each record has.
``max_cardinality``  The maximum number of this tag or subfield that each record has.
``samples``          Non-repeating sample values of the values of each tag or subfield.
=================    ==============================================================
