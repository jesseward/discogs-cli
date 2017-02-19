from pygments.lexer import RegexLexer, bygroups
from pygments.token import Text, String, Keyword, Name, Operator

__all__ = ['DiscogsCliLexer']


class DiscogsCliLexer(RegexLexer):

    name = 'DiscogsCli'
    aliases = ['discogs-cli']
    filenames = ['*.discogs-cli']

    tokens = {
        'root': [
            (r'(ogs)\s+', Keyword),
            (r'(\w+)(\s+)(\d+)', bygroups(Keyword, Text, String)),
            (r'(\w+)(\s+)(--lookup\s+\w+)?(\s+)?([\"\w\s]+)',
             bygroups(Keyword, Text, Operator, Text, String)),
            (r'(exit|quit)\s*', String, 'end'),
        ],
        'end': [
            (r'\n', Text, 'root')
        ],
    }
