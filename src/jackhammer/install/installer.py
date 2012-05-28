from abc import ABCMeta, abstractproperty, abstractmethod

import subprocess
from subprocess import call

import os,re,getpass

from fabric.operations import prompt,local

from jackhammer.utils import server
from jackhammer.utils.server import *
from jackhammer.utils.server import _test_mysql_connection

import json

class installer:
    __metaclass__ = ABCMeta

    db_details = None

    def __init__(self, dest, db_details=None, version="default"):
        self.dest, self.db_details, self.version = dest.rstrip("/"), db_details, version

        if not os.path.exists(self.dest):
            proceed = prompt("Destination %s doesn't exist, create and proceed?: " % self.dest, default="y")

            if proceed != "y":
                print "Aborting."
                import sys
                sys.exit()
            else:
                local("mkdir %s" % self.dest)
            
        self.devnull = open('/dev/null', 'w')

        self._retrieve_file()        
        self._extract_file()

        if self.db_details is None:
            self.db_details = self._database_details()
            
        self._modifying_files()
        self._prompt_for_details()
        self._install_package()
        self._clean_files()

    def _retrieve_file(self):
        """ Should check if the file exists already, and if so return (in the case of a failed
        attempt of installing). Otherwise it should download the file (based on version,
        revert to default from the packages manifest). """
        packages = json.load(open(json.load(get_server_config())["package_manifest"]))
        current_package = packages[self.package_name]

        self.package_filename = current_package["default"].split("/")[-1]

        try:
            open(self.package_filename)
        except IOError,e:
            subprocess.call(["wget", current_package["default"]],
                             stdout=self.devnull,
                             stderr=self.devnull)

        
        return

    def _extract_file(self):
        """ Should extract the file (using tar, or unzip, depending on the archive type) to the location,
        marked as self.dest. """
        return extract_archive(self.package_filename, self.dest)

    def _database_details(self):
        db_details = { "database_name": prompt("Database Name: "),
                       "database_user": prompt("Database User: ", default=getpass.getuser()),
                       "database_pass": re.escape(getpass.getpass("Database Password: ")),
                       "database_host": prompt("Database Host: ", default="localhost") }

        """ @todo
        db_test_conn = _test_mysql_connection(db_name=db_details["database_name"],
                                              username=db_details["database_user"],
                                              password=db_details["database_pass"],
                                              db_host=db_details["database_host"])

        if db_test_conn is None:
            print "MySQLdb module not installed, unable to test database connection, continuing."
            return db_details
        elif db_test_conn is False:
            print "Connection details failed."

            go_on = prompt("[c]ontinue  [a]bort  [r]etry:", default="r")

            if go_on == "r":
                return self._database_details()
            elif go_on == "c":
                return db_details
            else:
                import sys
                sys.exit()
        else: """
        return db_details
    
    @abstractmethod
    def _modifying_files(self):
        """ Package specific modifications really occur here, for example chmodding certain directories,
        removing readmes or other unneeded files. """
        return

    @abstractmethod
    def _prompt_for_details(self):
        """ Prompt the user for default values of the package, for example the WordPress admin username,
        as well as database information, base URLs, etc. """
        return
    
    @abstractmethod
    def _install_package(self):
        """ Covers the actual installation of the package, may involve calling a PHP file, or even
        database calls. """
        return

    @abstractmethod
    def _clean_files(self):
        """ Cleanup, anything that can be done after the installation, a good example is deleting
        the original archive that was downloaded. That should be done here in the case of failed
        installations. """
        return
