from abc import ABCMeta, abstractproperty, abstractmethod

import subprocess
from subprocess import call

from utils import server
from utils.server import get_server_config

import json

class installer:
    #__metaclass__ = ABCMeta

    def __init__(self, dest, version="default"):
        self.dest, self.version = dest, version

        # @todo - confirm dest exists and is a directory, or at least we can make the diro

        self.devnull = open('/dev/null', 'w')

        self._retrieve_file()        
        self._extract_file()
        self._modifying_files()
        self._prompt_for_details()
        self._install_package()
        self._clean_files()

    #@abstractmethod
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

    #@abstractmethod
    def _extract_file(self):
        """ Should extract the file (using tar, or unzip, depending on the archive type) to the location,
        marked as self.dest. """
        return

    #@abstractmethod
    def _modifying_files(self):
        """ Package specific modifications really occur here, for example chmodding certain directories,
        removing readmes or other unneeded files. """
        return

    #@abstractmethod
    def _prompt_for_details(self):
        """ Prompt the user for default values of the package, for example the WordPress admin username,
        as well as database information, base URLs, etc. """
        return
    
    #@abstractmethod
    def _install_package(self):
        """ Covers the actual installation of the package, may involve calling a PHP file, or even
        database calls. """
        return

    #@abstractmethod
    def _clean_files(self):
        """ Cleanup, anything that can be done after the installation, a good example is deleting
        the original archive that was downloaded. That should be done here in the case of failed
        installations. """
        return
