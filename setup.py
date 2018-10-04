from setuptools import setup, find_packages
from os import path
from mastojeppetto import VERSION

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(

    name='mastojeppetto',

    version=VERSION,

    description='A Mastodon/Pleroma emoji downloader',

    long_description=long_description,

    long_description_content_type='text/markdown',

    url='https://github.com/autoscatto/mastojeppetto',

    author='Perpli.me',

    author_email='4utoscatto@gmail.com',

    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='mastodon pleroma development download downloader',
    packages=['mastojeppetto/'],
    install_requires=['requests'],
    extras_require={  # Optional
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # `pip` to create the appropriate form of executable for the target
    # platform.
    #
    # For example, the following would provide a command called `sample` which
    # executes the function `main` from this package when invoked:
    entry_points={
        'console_scripts': [
            'mastojeppetto=mastojeppetto:main',
        ],
    },

    project_urls={
        'Bug Reports': 'https://github.com/autoscatto/mastojeppetto/issues',
        'Funding': 'https://donate.pypi.org',
        'Say Thanks!': 'https://saythanks.io/to/autoscatto',
        'Source': 'https://github.com/autoscatto/mastojeppetto/',
    },
)
