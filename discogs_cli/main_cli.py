#!/usr/bin/env python
# -*- coding: utf-8 -*-
import click
import sys

from .discogs import Release, Artist, Label

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
    except Exception as e:
        click.secho('Unable to fetch label id: {label_id} ({e})'.format(
            label_id=label_id, e=e), fg='red')
        sys.exit(1)


@cli.command('release')
@click.argument('release_id')
def release(release_id):
    """Retrieve a single release from the discogs database."""
    r = Release(release_id)

    try:
        r.show()
    except Exception as e:
        click.secho('Unable to fetch release id: {release_id} ({e})'.format(
            release_id=release_id, e=e), fg='red')
        sys.exit(1)


@cli.command('artist')
@click.argument('arist_id')
def artist(arist_id):
    """Retrieve artist information and their associated releases."""
    r = Artist(arist_id)
    try:
        r.show()
    except Exception as e:
        click.secho('Unable to fetch artist id: {arist_id} ({e})'.format(
            arist_id=arist_id, e=e), fg='red')
        sys.exit(1)


@cli.command('search')
@click.argument('q')
def search(q):
    """Search for Discogs artist, release, label information."""
    click.secho('Not yet implmented.', fg='red')

if __name__ == '__main__':
    cli()
