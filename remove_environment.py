from environment.environment import *

from project import project
from project.project import *

from optparse import OptionParser

# @todo --type should be able to be computed via the env_config.json once it's complete
# Remove Environment
# python remove_environment.py --user dlamanna --project nysba --type development --preserve-db
"""
Removing an enviornment, possibly keeping the database.
"""

opt_parser = OptionParser()
opt_parser.add_option("-u", "--user",        dest="username")
opt_parser.add_option("-p", "--project",     dest="project")
opt_parser.add_option("-t", "--type",        dest="env_type", help="Type of environment, must be: development, staging, or production")
opt_parser.add_option("-d", "--preserve-db", dest="preserve_db")

(options, args) = opt_parser.parse_args()

if not project_exists_in_manifest(options.project):
    print "Project does not exist in manifest, try creating it first."
    import sys
    sys.exit()
else:
    env = environment(options.username, options.project, options.env_type)

    preserve_db = True if options.preserve_db else False
    
    env.remove_environment(preserve_db)
