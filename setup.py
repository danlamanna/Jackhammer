#!/usr/bin/env python

from distutils.core import setup

setup(name='jackhammer',
      version='0.1dev',
      description='Jackhammer Deployment Utilities',
      author='Dan Lammana, Chris Kotfila',
      author_email='dev@burstmarketing.net',
      url='http://burstmarketing.net',
      package_dir = {'': 'src' },
      packages = ['jackhammer', 
      'jackhammer.database', 
      'jackhammer.install', 
      'jackhammer.environment', 
      'jackhammer.migration', 
      'jackhammer.project', 
      'jackhammer.vc', 
      'jackhammer.utils'],
      provides = ['jackhammer'],
      scripts = ['scripts/jackhammer'],
      package_data={'jackhammer': ['etc/server_config.json']},
      
      
      
    )
