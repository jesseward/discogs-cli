# -*- coding: utf-8 -*-

import subprocess

import click
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles import style_from_pygments_cls
from pygments.styles import get_style_by_name

from .__init__ import __version__

# from .completion import command_completer
from .ext.completer import Completer
from .ext.utils import TextUtils
from .pyglexer import DiscogsCliLexer

EXIT = ["quit", "exit", "logoff", "sys64738"]
TOKEN = "ogs "


def execute(cmd):
    # TODO: BUG: will not work on windows.
    PAGING = '|less -F -r -X --prompt "[space] for next page [q] to quit."'

    try:
        subprocess.call(cmd + PAGING, shell=True)
    except Exception as e:
        click.secho(e, fg="red")


def cli():
    history = InMemoryHistory()
    session = PromptSession(history=history)
    style = style_from_pygments_cls(get_style_by_name("monokai"))
    lexer = PygmentsLexer(DiscogsCliLexer)
    completer = Completer(fuzzy_match=False, text_utils=TextUtils())

    SYNTAX = "Syntax: ogs <command> [options]"

    click.secho(r"     _ _                                    _ _ ", fg="yellow")
    click.secho(r"  __| (_)___  ___ ___   __ _ ___        ___| (_)", fg="yellow")
    click.secho(r" / _` | / __|/ __/ _ \ / _` / __|_____ / __| | |", fg="yellow")
    click.secho(r"| (_| | \__ \ (_| (_) | (_| \__ \_____| (__| | |", fg="yellow")
    click.secho(r" \__,_|_|___/\___\___/ \__, |___/      \___|_|_|", fg="yellow")
    click.secho(r"                       |___/", fg="yellow")

    click.echo("Version:" + __version__)
    click.echo(SYNTAX)

    while True:
        try:
            text = session.prompt(
                "discogs-cli >>> ",
                style=style,
                completer=completer,
                lexer=lexer,
            )
        except EOFError:
            break

        if text in EXIT:
            break

        if text.startswith(TOKEN):
            execute(text)
        else:
            click.secho("Guru meditation error. " + SYNTAX, fg="red")


if __name__ == "__main__":
    cli()
