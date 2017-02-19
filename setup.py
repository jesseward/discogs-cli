import io
from discogs_cli.__init__ import __version__


try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup


description = 'View and search for artists, labels and releases in the Discogs.com library, from the command line.'
try:
    with io.open('README.rst', encoding="utf-8") as fh:
            long_description = fh.read()
except IOError:
    long_description = description


setup(
    name='discogs-cli',
    description=description,
    long_description=long_description,
    author='Jesse Ward',
    author_email='jesse@jesseward.com',
    version=__version__,
    url='https://github.com/jesseward/discogs-cli',
    license='MIT',
    install_requires=[
        'Pygments==2.2.0',
        'click==6.7',
        'discogs-client==2.2.1',
        'prompt-toolkit==1.0.13',
        'requests==2.13.0',
    ],
    entry_points={
        'console_scripts': [
            'discogs-cli = discogs_cli.main:cli',
            'ogs = discogs_cli.main_cli:cli',
        ]
    },
    packages=find_packages(),
    scripts=[],
    classifiers=[
        'Environment :: Console',
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
