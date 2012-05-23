import subprocess
from subprocess import call

import optparse

class magento_installer:

    op = optparse.OptionParser()

    magento_details = {}

    devnull = open('/dev/null', 'w')
    
    def __init__(self):
        self.op.add_option('--verbose', '-v', action="store_true", dest="verbose")
        self.op.add_option('--dest',    '-d', default="magento",   dest="dest")
        self.options, self.args = self.op.parse_args()

        self.filename = "magento-1.7.0.0.tar.gz"

        self._retrieve_file()
        self._extract_file()
        self._move_files()
        self._modifying_files()
        self._prompt_for_details()
        self._install_magento()
        self._clean_files()

    def log_if_verbose(self, message):
        if self.options.verbose is True:
            print message

    def _retrieve_file(self):
        try:
            open(self.filename)
            
            self.log_if_verbose(self.filename + " file exists already, using it.")

        except IOError:
            self.log_if_verbose("Downloading " + self.filename + " ....")

            subprocess.call(["wget", "http://www.magentocommerce.com/downloads/assets/1.7.0.0/magento-1.7.0.0.tar.gz"],
                            stdout=self.devnull,
                            stderr=self.devnull)
        
            self.log_if_verbose("Retrieved magento-1.7.0.0.tar.gz")

    
    def _extract_file(self):
        subprocess.call(["tar", "-zxvf", self.filename],
                        stdout=self.devnull,
                        stderr=self.devnull)
        
        self.log_if_verbose("Extracted magento-1.7.0.0.tar.gz to ./magento ")
        
    def _move_files(self):
        if self.options.dest is not "magento":
            import shutil
            shutil.copytree("magento", self.options.dest)

        self.log_if_verbose("Moving files from ./magento to " + self.options.dest)

    def _modifying_files(self):
        subprocess.call(["chmod", "-R", "o+w", "media", "var"],
                        stdout=self.devnull,
                        stderr=self.devnull)

        subprocess.call(["chmod", "o+w", "app/etc"],
                        stdout=self.devnull,
                        stderr=self.devnull)

        self.log_if_verbose("Modifying permissions...")

    def _prompt_for_details(self):
        default_host = "localhost"

        self.magento_details["db_username"] = "dlamanna"#raw_input("Database Username: ")
        self.magento_details["db_password"] = ""#raw_input("Password: ")
        self.magento_details["db_name"]     = "dlamanna_testinstaller"#raw_input("Database Name?: ")
        self.magento_details["db_host"]     = "localhost"#raw_input("Please enter name: %s" % default_host + chr(8)*4)
        self.magento_details["admin_pass"]  = ""#raw_input("Admin Password?: ")
        self.magento_details["store_url"]   = "http://dlamanna.testinstaller.dev.com/"#raw_input("Store Url (with trailing slash): ")

        if not self.magento_details["db_host"]:
            self.magento_details["db_host"] = default_host

    def _install_magento(self):
        php_string = "php --file %s/install.php" % self.options.dest
        print php_string
        subprocess.call(php_string)
    
    def _clean_files(self):
        import shutil, os

        shutil.rmtree("magento")
        #os.remove(self.filename)

        self.log_if_verbose("Removing original directory, and retrieved file - " + self.filename)
        


if __name__ == '__main__':
    magento_installer()



