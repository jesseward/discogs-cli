#!/usr/bin/env python
from __future__ import unicode_literals

from prompt_toolkit.contrib.completers import WordCompleter


command_completer = WordCompleter([
    'album',
    'artist',
    'label',
    'search',
    'quit',
], ignore_case=True)
