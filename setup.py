from discogs_cli.__init__ import __version__

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

setup(
    description=('View and search for artists, labels and releases in the Discogs.com library, from the command line.'),
    author='Jesse Ward',
    author_email='jesse@jesseward.com',
    version=__version__,
    install_requires=[
        'Pygments>=2.1.3',
        'click>=6.6',
        'discogs-client==2.2.1',
        'prompt-toolkit>=1.0.0',
        'requests>=2.10.0',
    ],
    entry_points={
        'console_scripts': [
            'discogs-cli = discogs_cli.main:cli',
            'ogs = discogs_cli.main_cli:cli',
        ]
    },
    packages=find_packages(),
    scripts=[],
    name='discogs-cli',
)
