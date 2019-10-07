#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import click

from .__init__ import __version__
from discogs_client import Client


class Discogs(object):
    """Wraps the discogs_client library. Encapsulating Search, Artist
    Release, Master, Label objects. Utility functionality in order to
    render output for terminal consumption.

    :type APP_VERSION: str (Const)
    :param APP_VERSION: Version of discogs-cli

    :type HEADER_COLOUR: str (const)
    :param HEADER_COLOUR: ANSI colour configuration for header records

    :type LABEL_COLOUR: str (const)
    :param LABEL_COLOUR: ANSI colour representation for column label fields.

    :type ID_COLOUR: str (const)
    :param ID_COLOUR: ANSI colour config for discogs id fields.

    :type client: :class:`discogs_client.client.Client`
    :param client: An instance of `discogs_client.client.Client`
    """

    APP_VERSION = 'discogs-cli/' + __version__
    HEADER_COLOUR = 'yellow'
    LABEL_COLOUR = 'cyan'
    ID_COLOUR = 'blue'

    def __init__(self, user_token=None):
        self.client = Client(Discogs.APP_VERSION, user_token=user_token)

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
        :param label: A string representing discogs id.

        :rtype: str
        :return: ANSI formatted string containing a discogs id."""
        return click.style(discogs_id, fg=Discogs.ID_COLOUR)

    def _artists(self, artists):
        """Formats the artist name and database id.

        :type artists: list
        :param artists: A list containing 1 or more artists data structures.

        :rtype: list
        :return: List of formatted artist names and ids."""

        try:
            return ['{name} [{id}]'.format(name=x['name'],
                id=self.cid(str(x['id']))) for x in artists]
        except TypeError:
            return []

    def _labels(self, labels):
        """Generates output string containing label and label id details.

        :type labels: list
        :param labels: List containing 1 or more labels data structures."""
        return self._artists(labels)

    def _separator(self, title):
        """Renders the ASCII delimiter/separator

        :type title: str
        :param title: A string representing the delimiter title.

        :rtype: str
        :return: A formatted string."""
        MAX = 50
        LEFT = 4
        RIGHT = 3
        return (
          ' -- [ ' + click.style(title, fg=Discogs.LABEL_COLOUR) + ' ] {line}'.
                format(title=title, line='-' * (MAX - 4 - len(title) - RIGHT)))

    def _page_artists(self, artists, page=1, end=1):
        """Renders a paginated list of Artist objects.

        :type artists:
        :param title: Paginated list containing artist objects."""

        while page <= end:
            for r in artists.page(page):
                click.echo('{artist} [{id}]'.format(artist=r.name,
                        id=self.cid(str(r.id))), color=True)
            page += 1

    def _page_labels(self, labels, page=1, end=1):
        return self._page_artists(labels, page=page, end=end)

    def _page_releases(self, releases, page=1, end=1, show_artist=False):

        if not show_artist:
            artist = ''

        while page <= end:
            for r in releases.page(page):
                if show_artist:
                    artist = r.data['artist'] + ' - '
                year = getattr(r, 'year', 'MASTER')
                click.echo('{year}\t{artist}{title} [{id}]'.format(year=year,
                title=r.title, id=self.cid(str(r.id)), artist=artist),
                color=True)
            page += 1


class Search(Discogs):
    """Performs a search against discogs Artists, Releases or Labels

    :type q: str
    :param q: Query string.

    :type q_type: str
    :param q_type: Type of query to perform release, artist or label.

    :type user_token: str
    :param user_token: A string containing your discogs.com user_token."""

    def __init__(self, q, q_type='release', user_token=None):
        super(Search, self).__init__(user_token=user_token)
        self.discogs = self.client.search(q, type=q_type)
        self.q = q
        self.q_type = q_type

    def show(self):

        out = []
        out.append(self._separator('{n} {qt}(s) matching "{q}"').format(
            q=self.q, qt=self.q_type, n=self.discogs.count))
        click.echo('\n'.join(out), color=True)

        if self.q_type == 'release':
            self._page_releases(self.discogs, end=self.discogs.pages)
        elif self.q_type == 'artist':
            self._page_artists(self.discogs, end=self.discogs.pages)
        elif self.q_type == 'label':
            self._page_labels(self.discogs, end=self.discogs.pages)


class Label(Discogs):
    """Displays a Discogs Label and its associated releases.

    :type label_id: int
    :param label_id: Discogs label id"""

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
        out.append('{prof}'.format(prof=self.discogs.data.get(
            'profile', 'None.')))
        out.append(self._separator('URLS'))
        out.append('{url}'.format(url='\n'.join(self.discogs.data.get('urls',
            ['None']))))
        out.append(self._separator('Releases'))
        click.echo('\n'.join(out), color=True)

        self._page_releases(self.discogs.releases, page=1, end=
                            self.discogs.releases.pages, show_artist=True)


class Artist(Discogs):
    """
    Nightmares On Wax
    Members     : George Evelyn [640294], Kevin Harper [427445], Robin Taylor-Firth [31653]
    Variations  : N O W, N.O.W, N.O.W., Nightmare On Wax, Nights On Wax, NoW
    In groups   :
     --[ Profile ] ------------------------------------
    The longest serving artist on the Warp Records roster. Originally founded in 1988 by
    George "DJ E.A.S.E." Evelyn and Kevin "Boywonder" Harper. Harper left before the
    release of Smokers Delight. When playing live they were also joined by MC Toz 180
    and guitarist Chris Dawkins.

    :type artist_id: int
    :param artist_id: A Discogs artist id."""

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
        click.echo('\n'.join(out), color=True)
        self._page_releases(self.discogs.releases, page=1, end=
                            self.discogs.releases.pages)


class Master(Discogs):
    """Displays a master release and its associated releases.

       :type master_id: int
       :param master_id: A Discogs master release id."""

    def __init__(self, master_id):
        super(Master, self).__init__()
        self.master_id = master_id
        self.discogs = self.client.master(self.master_id)

    def show(self):
        out = []

        out.append(self.cheader(self.discogs.title))
        out.append(self._separator('Versions'))
        click.echo('\n'.join(out), color=True)
        self._page_releases(self.discogs.versions, page=1, end=
                            self.discogs.versions.pages)


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

    :type release_id: int
    :param release_id: A Discogs.com release id.
    """

    def __init__(self, release_id, exclude="None", include="All"):
        super(Release, self).__init__()
        self.release_id = release_id
        self.discogs = self.client.release(self.release_id)
        self.exclude = exclude
        self.include = include


    def show(self):
        out = []
        year = self.discogs.year
        extraartists = self.discogs.data["extraartists"]
        out.append('{artists} - {title}'.format(artists=','.join(
            self._artists(self.discogs.data['artists'])),
            title=self.discogs.data['title']))

        labels = ['{label} ({cat}) [{id}]'.format(label=x.get('name'), cat=
            x.get('catno'), id=self.cid(str(x.get('id'))))
            for x in self.discogs.data['labels']]
        out.append(self.clabel('Label:') + '    {labels}'.format(
            labels=', '.join(labels)))

        formats = ['{name} ({desc})'.format(name=x.get('name'),
            desc=', '.join(x.get('descriptions', [])))
                    for x in self.discogs.data['formats']]
        out.append(self.clabel('Format:') + '   {name}'.format(name=','.join(
            formats)))

        out.append(self.clabel('Country:') + '  {country}'.format(
            country=self.discogs.country))
        out.append(self.clabel('Year:') + '     {year}'.format(year=year))
        out.append(self.clabel('Genre:') + '    {genre}'.format(genre=', '.join(
            self.discogs.genres)))
        try:
            out.append(self.clabel('Style:') + '    {style}'.format(style=', '.join(
                self.discogs.styles)))
        except:
            print("Style info not available.")
        out.append(self.clabel('Rating:') + '   {rating}/5'.format(
            rating=self.discogs.data.get('community', {}).get('rating',
                    {}).get('average'))) 
        out = self.show_extra(self.exclude,self.include,out)
        click.echo('\n'.join(out), color=True)

    def show_extra(self,exclude,include,out):
        personnel,tracklist,notes = True,True,True
        if "personnel" in exclude:
            personnel = False
        elif "tracklist" in exclude:
            tracklist = False
        elif "notes" in exclude:
            notes = False
        elif "personnel" in include:
            tracklist,notes = False,False
        elif "tracklist" in include:
            personnel,notes = False,False
        elif "notes" in include:
            personnel,tracklist = False,False

        if personnel is True:
            out.append(self._separator('Personnel'))
            for t in self.discogs.data['extraartists']:
                name = t["name"]
                role = t["role"]
                out.append(self.clabel('{role}: '.format(role=role)) + ' {name}'.format(
                    name=name))
        if tracklist is True:
            out.append(self._separator('Tracklist'))
            for t in self.discogs.data['tracklist']:
                duration = '   {0}'.format(t.get('duration'))
                out.append('{pos}\t{title} {dur}'.format(
                    pos=t['position'], title=t['title'], dur=duration))
        if notes is True:      
            out.append(self._separator('Notes'))
            out.append(self.discogs.data.get('notes', 'None.'))
        return out