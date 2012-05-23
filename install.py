from install import wp_installer
from install.wp_installer import *

from optparse import OptionParser

opt_parser = OptionParser()
opt_parser.add_option("-p", "--package", dest="package", help="Package to install, allowed values: wordpress, magento, codeigniter")
opt_parser.add_option("-d", "--dest",    dest="dest",    help="Destination directory to install to, must exist.")

(options, args) = opt_parser.parse_args()

#import ipdb; ipdb.set_trace()
if options.package == "wordpress":
    wp = wp_installer(options.dest)
