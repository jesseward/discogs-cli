#!/usr/bin/env python
# -*- coding: utf-8 -*-
import click
import os
import sys

from .discogs import Release, Artist, Label, Search, Master

import requests
requests.packages.urllib3.disable_warnings()


@click.group()
def cli():
    pass


@cli.command('label')
@click.argument('label_id')
def label(label_id):
    """Retrieve record label data and its associated releases."""
    r = Label(label_id)

    try:
        r.show()
    except IOError as e:
        pass
    except Exception as e:
        click.secho('Unable to fetch label id: {label_id} ({e})'.format(
            label_id=label_id, e=e), fg='red')


@cli.command('release')
@click.argument('release_id')
@click.option('--exclude', default="None")
@click.option('--include', default="All")
def release(release_id,exclude,include):
    """Retrieve a single release from the discogs database."""
    r = Release(release_id,exclude=exclude,include=include)

    try:
        r.show()
    except Exception as e:
        click.secho('Unable to fetch release id: {release_id} ({e})'.format(
            release_id=release_id, e=e), fg='red')


@cli.command('artist')
@click.argument('artist_id')
def artist(artist_id):
    """Retrieve artist information and their associated releases."""
    r = Artist(artist_id)
    try:
        r.show()
    except IOError as e:
        pass
    except Exception as e:
        click.secho('Unable to fetch artist id: {artist_id} ({e})'.format(
            artist_id=artist_id, e=e), fg='red')


@cli.command('master')
@click.argument('master_id')
def artist(master_id):
    """Retrieve master release information and their associated versions."""
    r = Master(master_id)
    try:
        r.show()
    except IOError as e:
        pass
    except Exception as e:
        click.secho('Unable to fetch master id: {master_id} ({e})'.format(
            master_id=master_id, e=e), fg='red')


@cli.command('search')
@click.argument('query')
@click.option('--lookup', default='release')
def search(query, lookup):
    """Search for Discogs artist, release, label information."""

    token = os.environ.get('TOKEN')
    if not token:
        click.secho('Unable to read your user_token. try export TOKEN=your_discogs_token_here',
                    fg='red')
    else:
        s = Search(query, q_type=lookup, user_token=token)

        try:
            s.show()
        except IOError as e:
            pass
        except Exception as e:
            click.secho('Unable to perform a {t} search for {q} ({e})'.format(
                 t=lookup, q=query, e=e), fg='red')

if __name__ == '__main__':
    cli()
