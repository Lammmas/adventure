try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Adventure Game',
    'author': 'Renna Reemet',
    'url': 'http://',
    'download_url': 'http://',
    'author_email': 'renna@devpurr.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['adventure'],
    'scripts': [],
    'name': 'adventure'
}

setup(**config)