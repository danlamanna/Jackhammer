#!/usr/bin/env python

from distutils.core import setup
import os

if not os.path.exists("/etc/jackhammer"):
        os.makedirs("/etc/jackhammer")


setup(name='jackhammer',
      version='0.1dev',
      description='Jackhammer Deployment Utilities',
      author='Dan LaManna, Chris Kotfila',
      author_email='dan.lamanna@gmail.com',
      url='http://danlamanna.com',
      package_dir = {'jackhammer': 'src/jackhammer' },
      packages = ['jackhammer', 
      'jackhammer.database', 
      'jackhammer.install', 
      'jackhammer.environment', 
      'jackhammer.project',
      'jackhammer.tasks',
      'jackhammer.vc', 
      'jackhammer.utils'],
      provides = ['jackhammer'],
      scripts = ['scripts/jh'],
      data_files=[('/etc/jackhammer', ['etc/server_config.json','etc/packages.json']),
                  ('/etc/jackhammer/skel', ['etc/skel/mysql_add_project_db.sql',
                                            'etc/skel/user.conf',
                                            'etc/skel/project.conf',
                                            'etc/skel/mysql_add_user.sql']),
                  ('/etc/jackhammer/skel/wp_install', ['etc/skel/wp_install/installer.php']),
                  ('/etc/jackhammer/skel/environment', ['etc/skel/environment/env_config.json']),
                  ('/etc/jackhammer/sql', [ 'etc/sql/drop_user.sql',
                                            'etc//sql/add_user.sql',
                                            'etc/sql/grant_privs.sql',
                                            'etc/sql/add_db.sql',
                                            'etc/sql/drop_db.sql' ])
                                            ]
        )
