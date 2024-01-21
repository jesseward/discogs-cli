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
        'opts': ''
    },
    'release': {
        'args': '1',
        'opts': [
            '--exclude (personnel|tracklist|notes)',
            '--include (personnel|tracklist|notes)'
        ]
    },
    'search': {
        'args': '"query string"',
        'opts': [
            '--lookup (artist|label|release)',
        ]
    },
}
META_LOOKUP = {
    '1': 'id: int - discogs ID to retrieve',
    '--lookup': '(artist|label|release)',
    '--exclude': '(personnel|tracklist|notes)',
    '--include': '(personnel|tracklist|notes)'
}
META_LOOKUP.update(SUBCOMMANDS)
