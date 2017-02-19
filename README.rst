.. figure:: http://www.jesseward.com/github/discogs-cli.gif
   :alt: image

   image

discogs-cli
===========

discogs-cli bring the Discogs.com database to your terminal. Perform the
following actions from your terminal

-  Search artists, releases, labels
-  View artist information and their releases
-  View label details and its associated releases
-  View a release in detail

Access to search functionality
------------------------------

Discogs requires `authentication`_ when accessing the search APIs. If
you wish to use the search functionality, you’re required to generate a
personal access token for your discogs.com account. You can do so at
https://www.discogs.com/settings/developers by clicking generate new
token.

Before starting your application set the ``TOKEN`` shell variable. where
``sys64738`` is your unique access token.

::

    $ export TOKEN=sys64738

Installation
------------

To install from PyPi, please use ``pip`` or ``easy_install``. For
example

::

    $ pip install discogs-cli

or

::

    $ easy_install discogs-cli

Note that installing into a ``virtualenv`` is generally recommended. If
you wish to install the latest and greatest via github source, please
ensure you’ve created a virtual environment.

::

    $ virtualenv ~/.virtualenv/discogs-cli
    $ source ~/.virtualenv/discogs-cli/bin/activate

Fetch and install the package from github

::

    $ pip install git+https://github.com/jesseward/discogs-cli.git

Once installed, run ``discogs-cli`` to launch the interactive command
prompt.

::

    $ discogs-cli

To launch commands from the console

::

    $ ogs <command> [params] [options]

TODO
----

-  Currently runs on a Unix like operating system only (Linux/OSX). If
   you can test and patch use for windows, please log a pull request.

About
-----

discogs-cli builds upon the following awesome Python libraries \* The
python-prompt-toolkit
https://github.com/jonathanslenders/python-prompt-toolkit \* Discogs.com
api client https://github.com/discogs/discogs\_client \* Haxor-news
string completion library https://github.com/donnemartin/haxor-news

.. _authentication: https://www.discogs.com/developers/#page:authentication
