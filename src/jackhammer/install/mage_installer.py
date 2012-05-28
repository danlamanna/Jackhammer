from fabric.operations import local, prompt

import subprocess
from subprocess import call

from jackhammer.utils import server
from jackhammer.utils.server import get_server_config, getpass_validate_regexp

import jackhammer.installer
import json, getpass

class mage_installer(installer.installer):

    package_name     = "magento"
    package_filename = None
    dest             = None
    version          = None

    install_details  = {}
    
    def _modifying_files(self):
        local("mv %(dest)s/magento/* %(dest)s"           % { "dest": self.dest })
        local("chmod -R o+w %(dest)s/media %(dest)s/var" % { "dest": self.dest })
        local("chmod o+w %(dest)s/app/etc"               % { "dest": self.dest })

    def _prompt_for_details(self):
        self.install_details["admin_email"]    = prompt("Admin Email: ", validate="[^@]+@[^@]+\.[^@]+")
        self.install_details["admin_username"] = prompt("Admin User: ", default="admin")
        self.install_details["admin_pass"]     = getpass_validate_regexp("Admin Password: ", "^\w{7,25}$")
        self.install_details["store_url"]      = prompt("Store URL: ").rstrip("/") + "/"

    def _install_package(self):
        local('php -f %(dest)s/install.php -- --license_agreement_accepted "yes" --locale "en_US" --timezone "America/New_York" --default_currency "USD" --db_host "%(db_host)s" --db_name "%(db_name)s" --db_user "%(db_user)s" --db_pass "%(db_pass)s" --url "%(store_url)s" --use_rewrites "yes" --use_secure "no" --use_secure_admin "no" --secure_base_url "" --admin_firstname "John" --admin_lastname "Doe" --admin_email "%(admin_email)s" --admin_username "%(admin_user)s" --admin_password "%(admin_pass)s"' %
              { "dest":        self.dest,
                "db_host":     self.db_details["database_host"],
                "db_name":     self.db_details["database_name"],
                "db_user":     self.db_details["database_user"],
                "db_pass":     self.db_details["database_pass"].replace("\\", ""),
                "store_url":   self.install_details["store_url"],
                "admin_email": self.install_details["admin_email"] ,
                "admin_user":  self.install_details["admin_username"],
                "admin_pass":  self.install_details["admin_pass"] })
    
    def _clean_files(self):
        local("rm -f %(package_filename)s" % { "package_filename": self.package_filename })
        local("rm -r %(dest)s/magento"     % { "dest":             self.dest })
        return True
