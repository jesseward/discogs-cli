![Imgur](http://i.imgur.com/iAXgnIj.gif)

# discogs-cli

discogs-cli bring the Discogs.com database to your terminal. Perform the following actions from your terminal

* Search artists, releases, labels
* View artist information and their releases
* View label details and its associated releases
* View a release in detail

## TODO
* Currently runs on a Unix like operating system only (Linux/OSX). If you can test and patch use for windows, please log a pull request.

## Installation

To install from the github source, please ensure you've created a virtual environment.

    $ virtualenv ~/.virtualenv/discogs-cli
    $ source ~/.virtualenv/discogs-cli/bin/activate

Fetch and install the package from github

    $ pip install git+https://github.com/jesseward/discogs-cli.git

Once installed, run `discogs-cli` to launch the interactive command prompt.

    $ discogs-cli

To launch commands from the console

    $ ogs <command> [params] [options]
