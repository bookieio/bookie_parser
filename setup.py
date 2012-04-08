from setuptools import setup, find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
NEWS = open(os.path.join(here, 'NEWS.txt')).read()

version = '0.1'

install_requires = [
    # List your project dependencies here.
    # For more details, see:
    # http://packages.python.org/distribute/setuptools.html#declaring-dependencies
    'lxml',
    'readability-lxml',
    'tornado',
]

tests_require = [
    'nose',
    'coverage',
    'webtest',
    'mock',
    'pylint',
    'pep8',
]


setup(name='bookie_parser',
    version=version,
    description="Readable and Content related tools for Bookie",
    long_description=README + '\n\n' + NEWS,
    classifiers=[
      # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    ],
    keywords='bookmarks content parsing readable tagging tags',
    author='Rick Harding',
    author_email='rharding@mitechie.com',
    url='docs.bmark.us',
    license='BSD',
    packages=find_packages('bookie_parser'),
    package_dir = {'': 'bookie_parser'},include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    tests_require=tests_require,
    entry_points={
        'console_scripts':
            ['bookie_parser=bookie_parser:main']
    }
)
