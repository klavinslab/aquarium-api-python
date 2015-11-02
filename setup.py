try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'coral',
    'author': 'Nick Bolten',
    'url': 'https://github.com/klavinslab/aquarium-api-python',
    'download_url': 'https://github.com/klavinslab/aquarium-api-python.git',
    'author_email': 'nbolten _at_ gmail',
    'version': '0.1.0',
    'install_requires': ['argparse', 'requests'],
    'packages': ['aquariumapi'],
    'scripts': [],
    'name': 'aquariumapi',
    'license': 'Copyright University of Washington'
}

setup(**config)
