from fabric.operations import get, local, prompt
from fabric.context_managers import cd

import subprocess
from subprocess import call

from utils import server
from utils.server import get_server_config

import installer

import json, getpass

class wp_installer(installer.installer):

    package_name     = "wordpress"
    package_filename = None
    dest             = None
    version          = None

    install_details  = {}

    def _retrieve_file(self):
        # @todo - this line is way too complicated to understand, break it up
        packages = json.load(open(json.load(get_server_config())["package_manifest"]))
        current_package = packages[self.package_name]

        self.package_filename = current_package["default"].split("/")[-1]

        try:
            open(self.package_filename)
        except IOError,e:
            subprocess.call(["wget", current_package["default"]],
                             stdout=self.devnull,
                             stderr=self.devnull)

    def _extract_file(self):
        if ".zip" not in self.package_filename:
            # @todo - Implement other methods of extraction
            return False
        else:            
            local("unzip %(archive)s -d %(dest)s" % { "archive": self.package_filename,
                                                      "dest":    self.dest })
            return

    def _modifying_files(self):
        local("mv %(dest)s/wordpress/* %(dest)s/" % { "dest": self.dest.rstrip("/") })

        # create wp-config.php
        # @todo - Enough of the rstrip business, set it in the init to remove trailing /
        config_file = self.dest.rstrip("/") + "/wp-config.php"
        sample_file = self.dest.rstrip("/") + "/wp-config-sample.php"

        local("cat %(sample)s > %(actual)s" % { "sample": sample_file,
                                                "actual": config_file })

        import re
        
        replace_mapping = { "database_name_here": prompt("Database Name: "),
                            "username_here":      prompt("Database User: "),
                            "password_here":      re.escape(getpass.getpass("Database Password: ")),
                            "localhost":          prompt("Database Host: ", default="localhost") }

        for string,replace in replace_mapping.iteritems():
            local("sed -i \"s/%(str)s/%(rep)s/g\" %(config_file)s" % { "str": string,
                                                                       "rep": replace,
                                                                       "config_file": config_file })
        return

    def _prompt_for_details(self):        
        self.install_details["blog_title"]  = prompt("Blog Title: ")
        self.install_details["site_url"]    = prompt("Site URL: ")
        self.install_details["admin_user"]  = prompt("Admin User: ")
        self.install_details["admin_email"] = prompt("Admin Email: ")
        self.install_details["admin_pass"]  = getpass.getpass("Admin Password: ")

        # @todo - validation? http://docs.fabfile.org/en/1.4.2/api/core/operations.html?highlight=prompt#fabric.operations.prompt

    def _install_package(self):
        # @todo - skel path is hardcoded for install module, set it as a config option
        local("cp skel/wp_install/installer.php %(dest)s" % { "dest": self.dest.rstrip("/") })

        install_mapping = { "site_url":    self.install_details["site_url"],
                            "blog_title":  self.install_details["blog_title"],
                            "admin_user":  self.install_details["admin_user"],
                            "admin_email": self.install_details["admin_email"],
                            "admin_pass":  self.install_details["admin_pass"] }

        import re
        for str,rep in install_mapping.iteritems():            
            local("sed -i 's/\${"+str+"}/"+re.escape(rep)+"/g' %(installer)s" % { "installer": self.dest.rstrip("/") + "/installer.php" })

        local("php -f %(install_file)s" % { "install_file": self.dest.rstrip("/") + "/installer.php" })        
        return
    

    def _clean_files(self):
        local("rm -rf %(dest)s/wordpress" % { "dest": self.dest.rstrip("/") })
        local("rm -f %s" % self.package_filename)
        return
