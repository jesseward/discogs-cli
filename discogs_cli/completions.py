# -*- coding: utf-8 -*-

SUBCOMMANDS = {
    'artist': 'Artist info and their releases',
    'label': 'Label and its associated releases',
    'master': 'Master release and child releases',
    'release': 'Release/Album data',
    'search': 'Search Discogs'
}
ARGS_OPTS_LOOKUP = {
    'artist': {
        'args': '1',
        'opts': '',
    },
    'label': {
        'args': '1',
        'opts': '',
    },
    'master': {
        'args': '1',
        'opts': '',
    },
    'release': {
        'args': '1',
        'opts': '',
    },
    'search': {
        'args': '"query string"',
        'opts': [
            '--lookup (artist|label|release)',
        ],
    },
}
META_LOOKUP = {
    '1': 'id: int - discogs ID to retrieve',
    '--lookup': '(artist|label|release)',
    '"(artist|label|release)"': 'Type of query to perform',
}
META_LOOKUP.update(SUBCOMMANDS)
