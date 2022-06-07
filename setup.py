"""Install the package."""

import os

from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


with open(os.path.join(os.path.dirname(__file__), 'requirements.txt'), encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line]

setup(
    name="bib-sanitizer",
    version="0.0.1",
    author='Benjamin Hilprecht',
    author_email='benjamin.hilprecht@cs.tu-darmstadt.de',
    description=("Use DBLP references instead"),
    # license = "Apache",
    keywords="latex bibtex references literature",
    packages=['bib_sanitizer'],
    long_description=read('README.md'),
    install_requires=requirements,
    classifiers=[
        "Development Status :: 3 - Alpha"
    ]
)