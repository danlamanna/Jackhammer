from install import wp_installer, mage_installer
from install.wp_installer import *
from install.mage_installer import *

from optparse import OptionParser

opt_parser = OptionParser()
opt_parser.add_option("-p", "--package", dest="package", help="Package to install, allowed values: wordpress, magento, codeigniter")
opt_parser.add_option("-d", "--dest",    dest="dest",    help="Destination directory to install to, must exist.")

(options, args) = opt_parser.parse_args()

if options.package == "wordpress":
    wp = wp_installer(options.dest)
elif options.package == "magento":
    mage = mage_installer(options.dest)
