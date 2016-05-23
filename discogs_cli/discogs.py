#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import click

from .__init__ import __version__
from discogs_client import Client


class Discogs(object):

    APP = 'discogs-cli/' + __version__
    HEADER_COLOUR = 'yellow'
    LABEL_COLOUR = 'cyan'
    ID_COLOUR = 'blue'

    def __init__(self):
        self.client = Client(Discogs.APP)

    def cheader(self, label):
        """Colour style for page header rows

        :type label: str
        :param label: A string representing the header value."""
        return click.style(label, fg=Discogs.HEADER_COLOUR)

    def clabel(self, label):
        """Colour style for label or column data.

        :type label: str
        :param label: A string representing the label value."""
        return click.style(label, fg=Discogs.LABEL_COLOUR)

    def cid(self, discogs_id):
        """Colour style for discogs id field.

        :type label: str
        :param label: A string representing discogs id."""
        return click.style(discogs_id, fg=Discogs.ID_COLOUR)

    def _artists(self, artists):
        """Formats the artist name and database id.

        :type artists: list
        :param artists: A list containing 1 or more artists data structures."""
        try:
            return [u'{name} [{id}]'.format(name=x['name'],
                id=self.cid(x['id'])) for x in artists]
        except TypeError:
            return []

    def _labels(self, labels):
        return self._artists(labels)

    def _separator(self, title):
        """Renders the ASCII delimiter/separator

        :type title: str
        :param title: A string representing the delimiter title."""
        MAX = 50
        LEFT = 4
        RIGHT = 3
        return (
          ' -- [ ' + click.style(title, fg=Discogs.LABEL_COLOUR) + ' ] {line}'.
                format(title=title, line='-' * (MAX - 4 - len(title) - RIGHT)))

    def _releases(self, releases, all=False, page=0, end=1):
        out = []

        if all == True:
            page = 1
            end = releases.pages

        while page <= end:
            for r in releases.page(page):
                year = getattr(r, 'year', u'MASTER')
                out.append(u'{year}\t{title} [{id}]'.format(year=year,
                title=r.title, id=self.cid(str(r.id))))
            page += 1
        return out


class Label(Discogs):

    def __init__(self, label_id):
        super(Label, self).__init__()
        self.label_id = label_id
        self.discogs = self.client.label(self.label_id)

    def show(self):
        out = []
        out.append(self.cheader(self.discogs.name))

        if self.discogs.parent_label is not None:
            out.append(self.clabel('Parent      :') + ' {parent} [{id}]'.
                    format(parent=self.discogs.parent_label.name,
                           id=self.cid(str(self.discogs.parent_label.id))))
        out.append(self.clabel('Sublabels   :') + ' {sublabels}'.format(
            sublabels=', '.join(self._labels(
                self.discogs.data.get('sublabels', [])))))
        out.append(self._separator('Profile'))
        out.append(u'{prof}'.format(prof=self.discogs.data.get(
            'profile', 'None.')))
        out.append(self._separator('URLS'))
        out.append(u'{url}'.format(url='\n'.join(self.discogs.data.get('urls',
            ['None']))))
        out.append(self._separator('Releases'))
        out = out + self._releases(self.discogs.releases)

        click.echo_via_pager('\n'.join(out))


class Artist(Discogs):
    """
    Nightmares On Wax
    Members     : George Evelyn [640294], Kevin Harper [427445], Robin Taylor-Firth [31653]
    Variations  : N O W, N.O.W, N.O.W., Nightmare On Wax, Nights On Wax, NoW
    In groups   :
     --[ Profile ] ------------------------------------
    The longest serving artist on the Warp Records roster. Originally founded in 1988 by George "DJ E.A.S.E." Evelyn and Kevin "Boywonder" Harper. Harper left before the release of Smokers Delight. When playing live they were also joined by MC Toz 180 and guitarist Chris Dawkins.
    """

    def __init__(self, artist_id):
        super(Artist, self).__init__()
        self.artist_id = artist_id
        self.discogs = self.client.artist(self.artist_id)

    def show(self):
        out = []

        out.append(self.cheader(self.discogs.name))
        out.append(self.clabel('Members     ') + ': {members}'.format(
            members=', '.join(self._artists(
                self.discogs.data.get('members', [])))))
        out.append(self.clabel('Variations  ') + ': {var}'.format(var=', '.join(
            self.discogs.data.get('namevariations', []))))
        out.append(self.clabel('In groups   ') + ': {groups}'.format(groups=
            ', '.join(self._artists(self.discogs.data.get('groups', [])))))
        out.append(self._separator('Profile'))
        out.append(self.discogs.data.get('profile', 'None.'))
        out.append(self._separator('Releases'))
        out = out + self._releases(self.discogs.releases)
        click.echo_via_pager('\n'.join(out))


class Release(Discogs):
    """
    Blunted Dummies [4130] - House For All
    Label:      Definitive Recordings (12DEF006) [934]
    Format:     Vinyl, 12", 33 ⅓ RPM
    Country:    Canada
    Released:   1993
    Genre:      Electronic
    Style:      House
    --[ Tracklist ] -----------------------------------
    A1  -   House For All (Original Mix)
    A2  -   House For All (House 4 All Robots Mix)
    --[ Notes ] ---------------------------------------
    "House For All (Original Mix)" was originally released on the Mad Trax E.P.
    """

    def __init__(self, release_id):
        super(Release, self).__init__()
        self.release_id = release_id

        self.discogs = self.client.release(self.release_id)

    def show(self):
        out = []
        year = self.discogs.year

        out.append(self.cheader('{artists} - {title}'.format(artists=','.join(
            self._artists(self.discogs.data['artists'])),
            title=self.discogs.data['title'])))

        labels = [u'{label} ({cat}) [{id}]'.format(label=x.get('name'), cat=
            x.get('catno'), id=self.cid(str(x.get('id'))))
            for x in self.discogs.data['labels']]
        out.append(self.clabel('Label:') + '    {labels}'.format(
            labels=', '.join(labels)))

        formats = [u'{name} ({desc})'.format(name=x.get('name'),
            desc=x.get('descriptions')) for x in self.discogs.data['formats']]
        out.append(self.clabel('Format:') + '   {name}'.format(name=','.join(
            formats)))

        out.append(self.clabel('Country:') + '  {country}'.format(
            country=self.discogs.country))
        out.append(self.clabel('Year:') + '     {year}'.format(year=year))
        out.append(self.clabel('Genre:') + '    {genre}'.format(genre=', '.join(
            self.discogs.genres)))
        out.append(self.clabel('Style:') + '    {style}'.format(style=', '.join(
            self.discogs.styles)))

        out.append(self._separator('Tracklist'))
        for t in self.discogs.data['tracklist']:
            out.append(u'{pos}\t{title}\t{artists}'.format(pos=t['position'],
                title=t['title'], artists=','.join(self._artists(
                    t.get('artists', [])))))

        out.append(self._separator('Notes'))
        out.append(self.discogs.data.get('notes', 'None.'))
        click.echo_via_pager('\n'.join(out))
