from distutils.core import setup
from setuptools import find_packages

setup(
    name='pygoa',
    version='0.1.dev',
    license='MIT',
    author='msicilia',
    author_email='msicilia@gmail.com',
    url='https://github.com/msicilia/pygoa',
    classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 2',
    ],
    keywords='bioinformatics',
    packages=find_packages(exclude=['docs', 'tests*', 'notebooks']),
    description="Metrics and analytics across Gene Ontology versions",
    long_description="Metrics and analytics across Gene Ontology versions",
)
