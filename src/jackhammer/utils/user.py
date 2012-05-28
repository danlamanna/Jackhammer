import pwd

from fabric.api import *

from fabric.operations import sudo,local

import getpass

import json

class user_utility:

    server_config = None
    user_config   = None

    def __init__(self, config_file):
        # should check many other things,
        # validate configs fully, ensure skeleton dirs/files exist, etc
        
        try:
            self.server_config = json.load(open(config_file))
            self.user_config   = self.server_config['user_config']

            self._validate_configs()
        except IOError, e:
            print "Configuration file %s couldn't be loaded." % config_file
        except Exception, e:
            print e

    def _validate_configs(self):
        # ensure default_group is an actual group
        group_exists = False
        
        import grp
        for group in grp.getgrall():
            if (group[0] == self.user_config['default_group']):
                group_exists = True
                break
            
        if not group_exists:
            raise Exception("default_group \"%s\" doesn't exist." % self.user_config['default_group'])
            return False
            
        return True

    def _user_exists(self, username):
        for p in pwd.getpwall():
            if (p.pw_name == username):
                return True
            
        return False

    def add_user(self, username, password):    
        if (self._user_exists(username)):
            print "A user with the username \"%s\" already exists." % username
            return
        else:
            local("useradd %(username)s -G %(group)s -d %(userdir)s" % { "username": username,
                                                                         "group":    self.user_config['default_group'],
                                                                         "userdir":  self.user_config['home_dir'] + '/' + username })
            
            local("echo \"%(password)s\" | passwd --stdin %(username)s" %  { "username": username,
                                                                         "password": password })
        
            local("chmod 711 %(userdir)s" % { "userdir": self.user_config['home_dir'] + '/' + username })
            
            self._setup_projects_dir(username, password)
            self._setup_confd(username)            
            self.add_mysql_user(username, password)

    def remove_user(self, username):
        if not self._user_exists(username):
            print "User \"%s\" doesn't exist." % username
            return False
        elif username is 'root':
            print "Let's not be silly."
            return False
        elif username is getpass.getuser(): # current user
            print "Can not remove yourself while logged in."
            return False
        else:
            # do actual checks, (uncommitted changes, etc)
            # give a flag to backup their home dir somewhere
            # call userdel
            local("userdel -rf %s" % username)

            # remove specific conf files
            local("rm -rf %(confd_dir)s/%(username)s.d %(confd_dir)s/%(username)s.conf" % { "confd_dir": self.server_config['httpd_confd_dir'],
                                                                                            "username":  username })
            
            # remove mysql user
            self.remove_mysql_user(username)
            
            # mysql databases?

    def _setup_confd(self, username):
        local("mkdir %(confd_dir)s/%(username)s.d" % { "confd_dir": self.server_config['httpd_confd_dir'],
                                                       "username":  username })

        skel_user_conf = open(self.server_config['skeleton_dir'] + '/' + self.server_config['skeleton_files']['httpd_user_conf'])
        user_conf      = burst_replace('username', username, skel_user_conf.read())
        
        dot_conf = open(self.server_config['httpd_confd_dir'] + '/' + username + '.conf', 'w+')
        dot_conf.write(user_conf)

        print "------- Wrote user.conf file %s." % self.server_config['httpd_confd_dir'] + '/' + username + '.conf'

    def _setup_projects_dir(self, username, password):
        projects_dir = "%(homedir)s/%(username)s/%(projectdir)s" % { "homedir":    self.user_config['home_dir'],
                                                                     "username":   username,
                                                                     "projectdir": self.user_config['projects_dir'] }
        
        local("mkdir " + projects_dir)

        local("chown -R %(username)s:%(group)s %(projectdir)s" % { "username":   username,
                                                                   "group":      self.user_config['default_group'],
                                                                   "projectdir": projects_dir })

        local("chmod g+s %(projectdir)s" % { "projectdir": projects_dir })

        local("htpasswd -b -c %(projectdir)s/.htpasswd %(username)s \"%(password)s\"" % { "projectdir": projects_dir,
                                                                                     "username":   username,
                                                                                     "password":   password })
        
        local("chown %(username)s:%(username)s %(projectdir)s/.htpasswd" % { "username":   username,
                                                                            "projectdir": projects_dir })


    def add_mysql_user(self, username, password):
        import re
        from string import strip
        
        add_user_sql = open(self.server_config['sql_skel_dir'] + '/add_user.sql')
        add_user_sql = add_user_sql.read()
        
        sql = burst_replace('username', username, add_user_sql)
        sql = burst_replace('password', password, sql)

        local("mysql -u%(username)s -p%(password)s -e \"%(query)s\"" % { "username": self.server_config['mysql_user']['username'],
                                                                         "password": re.escape(self.server_config['mysql_user']['password']),
                                                                         "query":    sql.replace('"', '\"').strip() })

    def remove_mysql_user(self, username):
        import re
        
        sql = burst_replace('username', username, open(self.server_config['sql_skel_dir'] + '/drop_user.sql').read())
        
        local("mysql -u%(username)s -p%(password)s -e \"%(query)s\"" % { "username": self.server_config['mysql_user']['username'],
                                                                         "password": re.escape(self.server_config['mysql_user']['password']),
                                                                         "query":    sql.replace('"', '\"').strip() })


def burst_replace(string, replacement, text):
    return text.replace('${' + string + '}', replacement)


def user_exists(username):
    for p in pwd.getpwall():
        if (p.pw_name == username):
            return True
        
    return False
