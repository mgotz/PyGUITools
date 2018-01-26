#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
setup script for my pyqt collection package
"""
import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='mg_pyguitools',
    version='1.1.0',
    
    packages=find_packages(), #automagically include all subfolders as packages
    
    license='MIT',
    long_description=read('README.txt'),
    
    author='Malte Gotz',
    author_email='malte.gotz@oncoray.de',
    url='https://github.com/mgotz/PyGUITools',
    
    install_requires=['matplotlib','formlayout']
)