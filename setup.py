#!/usr/bin/env python

from setuptools import setup

setup(
    name='LotR',
    version='1.0',
    description='LotR LCG',
    author='mebusw',
    author_email='mebusw@163.com',
    url='http://www.python.org/sigs/distutils-sig/',
    install_requires=['gunicorn', 'Django>=1.3', 'djangorestframework', 'simplejson'],
)
