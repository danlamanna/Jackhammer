from manifest import *
from utils.user import burst_replace
from utils.server import *

from project.project import *

from fabric.operations import local
from fabric.api import *

class environment:

    user     = None
    project  = None
    env_type = None

    project_config = None

    def __init__(self, user, project, env_type, env_url=None):
        self.user = user
        self.project = project
        self.env_type = env_type
        self.env_url  = env_url

        self.project_config = get_project_manifest()['projects'][project]

    def create(self):
        conf = json.load(get_server_config())
        self.conf = conf
        
        dir_name = self.project
        env_dir  = conf['user_config']['home_dir'] + '/' + self.user + '/' + conf['user_config']['projects_dir'] + '/' + dir_name
        db_name  = self.user + '_' + self.project + '_' + self.project_config['type']

        self.env_dir = env_dir

        import re,time

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
        local("cp -r %(env_skel_dir)s/* %(envdir)s" % { "env_skel_dir": conf['skeleton_dir'] + '/environment',
                                                        "envdir":        env_dir })

        env_config = env_config_skel  = open(conf["skeleton_dir"] + "/environment/env_config.json").read()
        # @todo - this is clearly a bit broken, as it uses the default user credentials and localhost ALWAYS
        env_replacements = { "env_type":       self.env_type,
                             "env_url":        self.env_url,
                             "env_project":    self.project,
                             "env_created_at": str(time.time()).split(".")[0],
                             "db_name":        db_name,
                             "db_user":        conf["mysql_user"]["username"],
                             "db_pass":        conf["mysql_user"]["password"],
                             "db_host":        "localhost" }

        # fill in env_config.json
        for k,v in env_replacements.iteritems():
            env_config = burst_replace(k, v, env_config)

        # write the replaced data
        env_config_file = open("%s/env_config.json" % env_dir, "w")
        env_config_file.write(env_config)
        env_config_file.close()

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
        
        return { "directory": env_dir,
                 "db_name":   db_name }

    def remove_environment(self, preserve_db=False):
        conf = json.load(get_server_config())
        self.conf = conf
        
        dir_name = self.project
        env_dir  = conf['user_config']['home_dir'] + '/' + self.user + '/' + conf['user_config']['projects_dir'] + '/' + dir_name
        db_name  = self.user + '_' + self.project + '_' + self.project_config['type']

        # delete env dir
        local("rm -r %(envdir)s" % { "envdir": env_dir })

        # delete httpd conf
        local("rm -f %(envconf)s" % { "envconf": conf["httpd_confd_dir"] + "/" + self.user + ".d/" + self.project + ".conf" })    

        if preserve_db is False:
            import re
            # drop database
            sql = burst_replace('db_name', db_name, open(conf['sql_skel_dir'] + '/drop_db.sql').read())

            local("mysql -u%(username)s -p%(password)s -e \"%(query)s\"" % { "username": conf['mysql_user']['username'],
                                                                             "password": re.escape(conf['mysql_user']['password']),
                                                                             "query":    sql.replace('"', '\"') })
        return

    def checkout(self):
        for path,repo in self.project_config['repos'].iteritems():
            path = self.env_dir + '/httpdocs/' + path.lstrip('/')
            
            if repo['type'] == 'svn':
                local("svn checkout " + repo['url'] + " " + path)

        local("chown -R %(username)s:%(group)s %(httpdocs_path)s" % { "username": self.user,
                                                                      "group":    self.conf['user_config']['default_group'],
                                                                      "httpdocs_path": self.env_dir + '/httpdocs' })
        
        return None

    def _get_next_highest_env_type(self):
        if self.env_type == "production":
            return False
        elif self.env_type == "staging":
            return "production"
        elif self.env_type == "development":
            return "staging"

    def pull_db(self):
        env_to_pull_from = self._get_next_highest_env_type()
        source_env       = get_project_environment(self.project, env_to_pull_from)

        if not env_to_pull_from:
            print "This is the definitive data source, no other environments to pull from."
            return
        elif not source_env:
            print "No higher project environment exists, no where to pull from."
            return
        else:
            # pull db using source_env info

        return
