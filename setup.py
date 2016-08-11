## setuptools  (https://pythonhosted.org/setuptools/setuptools.html)

from setuptools import setup, find_packages

setup(
    name = "rssdl",
    version = "0.1",
    packages = find_packages(exclude=['tests', 'demo']),
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 1 - Planning',
    ],

    entry_points = {
        'console_scripts': [
            'rssdl = rssdl.cli:cli',
        ],
    },
)
