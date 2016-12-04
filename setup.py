"""
Setup
"""

from setuptools import setup, find_packages
import os
import imperialism_remake.version as vs

HERE = os.path.abspath(os.path.dirname(__file__))

CLASSIFIERS = ['Development Status :: 2 - Pre-Alpha',
               'Intended Audience :: End Users/Desktop',
               'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
               'Operating System :: OS Independent',
               'Programming Language :: Python :: 3',
               'Topic :: Games/Entertainment :: Turn Based Strategy']

KEYWORDS = 'imperialism remake turn based strategy game open source'

def get_long_description():
    """
    Get the long description from the README file.
    """
    with open(os.path.join(HERE, 'README.md'), encoding='utf-8') as f:
        return f.read()

def get_data_files():
    """
    Get the list of data files (full content of data directory).
    """
    data_files = []
    for dirpath, dirnames, filenames in os.walk(os.path.join(HERE, 'data')):
        if filenames:
            destination = os.path.relpath(dirpath, HERE)
            names = [os.path.join(destination, name) for name in filenames]
            data_files.append((destination,names))
    return data_files

def get_data_files2():
    data_files = []
    for dirpath, dirnames, filenames in os.walk(os.path.join(HERE, 'data')):
        if filenames:
            destination = os.path.relpath(dirpath, HERE)
            names = [os.path.join(destination, name) for name in filenames]
            data_files.append(names)
    return data_files

if __name__ == "__main__":
    setup(name='imperialism_remake',
        version=vs.__version__,
        description='Open source remake of Imperialism',
        long_description=get_long_description(),
        url='http://remake.twelvepm.de/',
        author='Trilarion',
        author_email='pypi@twelvepm.de',
        license='GPL',
        classifiers=CLASSIFIERS,
        keywords=KEYWORDS,
        package_dir={'':'source'},
        packages=find_packages(where=os.path.join(HERE, 'source')),
        install_requires=['PyYAML>=3.1', 'PyQt5>=5.6'],
        #data_files=get_data_files(),
        package_data={'imperialism_remake': 'data'},
        entry_points={'console_scripts': ['imperialism_remake_start=imperialism_remake.imperialism_remake:main']},
        zip_safe=False)
