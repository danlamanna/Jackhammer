from manifest import *
from utils.user import burst_replace
from utils.server import *

from fabric.operations import local
from fabric.api import *

class environment:

    user     = None
    project  = None
    env_type = None

    project_config = None

    def __init__(self, user, project, env_type):
        self.user = user
        self.project = project
        self.env_type = env_type

        self.project_config = get_project_manifest()['projects'][project]

    def create(self):
        conf = json.load(get_server_config())
        self.conf = conf

        #import ipdb; ipdb.set_trace()
        dir_name = self.project
        env_dir  = conf['user_config']['home_dir'] + '/' + self.user + '/' + conf['user_config']['projects_dir'] + '/' + dir_name
        db_name  = self.user + '_' + self.project + '_' + self.project_config['type']

        self.env_dir = env_dir

        import re

        # create database, grant privs
        sql = burst_replace('db_name', db_name, open(conf['sql_skel_dir'] + '/add_db.sql').read())

        local("mysql -u%(username)s -p%(password)s -e \"%(query)s\"" % { "username": conf['mysql_user']['username'],
                                                                         "password": re.escape(conf['mysql_user']['password']),
                                                                         "query":    sql.replace('"', '\"') })

        sql = burst_replace('db_name', db_name, open(conf['sql_skel_dir'] + '/grant_privs.sql').read())
        sql = burst_replace('db_user', self.user, sql)

        local("mysql -u%(username)s -p%(password)s -e \"%(query)s\"" % { "username": conf['mysql_user']['username'],
                                                                         "password": re.escape(conf['mysql_user']['password']),
                                                                         "query":    sql.replace('"', '\"') })

        # setup env directory
        local("mkdir %s" % env_dir)
        local("cp -r %(proj_skel_dir)s/* %(envdir)s" % { "proj_skel_dir": conf['skeleton_dir'] + '/project',
                                                         "envdir":        env_dir })

        local("chown -R %(user)s:%(group)s %(envdir)s" % { "user":   self.user,
                                                           "group":  conf['user_config']['default_group'],
                                                           "envdir": env_dir })
        local("chmod g+s %(envdir)s" % { "envdir": env_dir })

        # add httpd conf
        httpd_conf = open(conf['skeleton_dir'] + '/project.conf').read()
        httpd_conf = burst_replace('username', self.user, httpd_conf)
        httpd_conf = burst_replace('project', self.project, httpd_conf)

        new_httpd_conf = open(conf['httpd_confd_dir'] + '/' + self.user + '.d/' + self.project + '.conf', 'w')
        new_httpd_conf.write(httpd_conf)
        new_httpd_conf.close()        

        # reload httpd
        local("/etc/init.d/httpd reload")
        
        return None

    # @todo - implement remove_environment

    def checkout(self):
        for path,repo in self.project_config['repos'].iteritems():
            path = self.env_dir + '/httpdocs/' + path.lstrip('/')
            
            if repo['type'] == 'svn':
                local("svn checkout " + repo['url'] + " " + path)

        local("chown -R %(username)s:%(group)s %(httpdocs_path)s" % { "username": self.user,
                                                                      "group":    self.conf['user_config']['default_group'],
                                                                      "httpdocs_path": self.env_dir + '/httpdocs' })
        
        return None

    def pull_db(self):
        print "Pulling Db...Not really."
        return None
