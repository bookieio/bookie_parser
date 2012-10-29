from setuptools import find_packages
from setuptools import setup
import os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
NEWS = open(os.path.join(here, 'NEWS.txt')).read()

version = '0.3'

install_requires = [
    'lxml',
    'breadability',
    'Mako',
    'pyramid==1.4a3'
    'pryamid_debugtoolbar',
    'waitress',
]

tests_require = [
    'nose',
    'coverage',
    'webtest',
    'mock',
    'pylint',
    'pep8',
]


setup(
    name='bookie_parser',
    version=version,
    description="Readable and Content related tools for Bookie",
    long_description=README + '\n\n' + NEWS,
    classifiers=[
        # Get strings from
        # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    ],
    keywords='bookmarks content parsing readable tagging tags',
    author='Rick Harding',
    author_email='rharding@mitechie.com',
    url='docs.bmark.us',
    license='BSD',
    packages=find_packages('bookie_parser'),
    package_dir={'': 'bookie_parser'},
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={'test': tests_require},
    entry_points="""\
    [paste.app_factory]
    main = bookie_parser:main
    [console_scripts]
    bookie_parser=bookie_parser:main
    """
)
