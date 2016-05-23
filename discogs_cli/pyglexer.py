from pygments.lexer import RegexLexer, bygroups
from pygments.token import Text, String, Keyword, Name, Operator


class DiscogsCliLexer(RegexLexer):

    name = 'DiscogsCli'
    aliases = ['discogs-cli']
    filenames = ['*.discogs-cli']

    tokens = {
        'root': [
            (r'\s+', Text),
            (r'(?i)(release|artist|label)(\s*)', Keyword),
            (r'exit\s*', Keyword, 'end'),
            (r'quit\s*', Keyword, 'end')
        ],
        'end': [
            (r'\n', Text, 'root')
        ],
    }
