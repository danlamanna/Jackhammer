from fabric.operations import get, local, prompt
from fabric.context_managers import cd

import subprocess
from subprocess import call

from utils import server
from utils.server import *

import installer, os

import json, getpass

class wp_installer(installer.installer):

    package_name     = "wordpress"
    package_filename = None
    dest             = None
    version          = None

    install_details  = {}

    def _modifying_files(self):
        local("mv %(dest)s/wordpress/* %(dest)s/" % { "dest": self.dest })
        
        config_file = self.dest + "/wp-config.php"
        sample_file = self.dest + "/wp-config-sample.php"

        local("cat %(sample)s > %(actual)s" % { "sample": sample_file,
                                                "actual": config_file })
        
        replace_mapping = { "database_name_here": self.db_details["database_name"],
                            "username_here":      self.db_details["database_user"],
                            "password_here":      self.db_details["database_pass"],
                            "localhost":          self.db_details["database_host"] }

        for string,replace in replace_mapping.iteritems():
            local("sed -i \"s/%(str)s/%(rep)s/g\" %(config_file)s" % { "str": string,
                                                                       "rep": replace,
                                                                       "config_file": config_file })
        return

    def _prompt_for_details(self):        
        self.install_details["blog_title"]  = prompt("Blog Title: ")
        self.install_details["site_url"]    = prompt("Site URL: ").rstrip("/")
        self.install_details["admin_user"]  = prompt("Admin User: ")
        self.install_details["admin_email"] = prompt("Admin Email: ", validate="[^@]+@[^@]+\.[^@]+")
        self.install_details["admin_pass"]  = getpass.getpass("Admin Password: ")

    def _install_package(self):
        # @todo - make install_skel_dir defined in installer, instead of getting it multiple times
        install_skel_dir = json.load(get_server_config())["install_skel_dir"]
        local("cp %(install_skel_dir)s/wp_install/* %(dest)s" % { "install_skel_dir": install_skel_dir,
                                                                  "dest":             self.dest })

        install_mapping = { "site_url":    self.install_details["site_url"],
                            "blog_title":  self.install_details["blog_title"],
                            "admin_user":  self.install_details["admin_user"],
                            "admin_email": self.install_details["admin_email"],
                            "admin_pass":  self.install_details["admin_pass"] }

        import re
        for str,rep in install_mapping.iteritems():            
            local("sed -i 's/\${"+str+"}/"+re.escape(rep)+"/g' %(installer)s" % { "installer": self.dest + "/installer.php" })

        local("php -f %(install_file)s" % { "install_file": self.dest + "/installer.php" })        
        return

    # @todo perhaps this could go in installer.py?
    def _remove_skeleton_files(self):
        install_skel_dir = json.load(get_server_config())["install_skel_dir"] + "/wp_install"

        for filename in os.listdir(install_skel_dir):
            local("rm -r %(dest)s/%(filename)s" % { "dest": self.dest,
                                                    "filename": filename })

    def _clean_files(self):
        local("rm -rf %(dest)s/wordpress" % { "dest": self.dest })
        local("rm -f %s" % self.package_filename)

        self._remove_skeleton_files()
        return
