# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import click
import subprocess
import sys

from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.layout.lexers import PygmentsLexer
from prompt_toolkit.styles.from_pygments import style_from_pygments
from pygments.styles import get_style_by_name

from .__init__ import __version__
from .completion import command_completer
from .discogs import Release, Artist, Label
from .pyglexer import DiscogsCliLexer


import requests
requests.packages.urllib3.disable_warnings()

EXIT = ['quit', 'exit', 'logoff', 'sys64738']
TOKEN = 'ogs '


def execute(cmd):
    try:
        subprocess.call(cmd, shell=True)
    except Exception as e:
        click.secho(e, fg='red')


def cli():
    history = InMemoryHistory()
    style = style_from_pygments(get_style_by_name('monokai'))
    lexer = PygmentsLexer(DiscogsCliLexer)

    click.secho('     _ _                                    _ _ ', fg='red')
    click.secho('  __| (_)___  ___ ___   __ _ ___        ___| (_)', fg='red')
    click.secho(' / _` | / __|/ __/ _ \ / _` / __|_____ / __| | |', fg='red')
    click.secho('| (_| | \__ \ (_| (_) | (_| \__ \_____| (__| | |', fg='red')
    click.secho(' \__,_|_|___/\___\___/ \__, |___/      \___|_|_|', fg='red')
    click.secho('                       |___/', fg='red')

    click.echo('Version:' + __version__)
    click.echo('Syntax: ogs <command> [options]')
    while True:

        try:
            text = prompt('discogs-cli >>> ', style=style, history=history,
                    lexer=lexer, completer=command_completer)
        except EOFError:
            break

        if text in EXIT:
            sys.exit(0)

        if text.startswith(TOKEN):
            execute(text)

if __name__ == '__main__':
    cli()
