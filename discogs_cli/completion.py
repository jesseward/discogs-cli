#!/usr/bin/env python
from __future__ import unicode_literals

from prompt_toolkit.contrib.completers import WordCompleter


command_completer = WordCompleter([
    'artist',
    'label',
    'master',
    'release',
    'search',
], meta_dict={
    'artist': 'Discogs artist id to retrive',
    'label': 'Discogs label id to retrieve',
    'master': 'Discogs master release id to fetch versions',
    'release': 'Discogs release id to retrieve',
    'search': 'Query Discogs based on keywords',
},
    ignore_case=True)
