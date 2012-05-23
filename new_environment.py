from utils import user
from utils.user import user_utility
from utils.user import user_exists

from project import project
from project.project import *
from manifest import get_project_manifest
from environment.environment import *

from fabric.operations import prompt

from optparse import OptionParser

username = None
project  = None
env_type = None

# Add User To Project
# python new_environment --user dlamanna --project nysba --type development --checkout --pull-db
"""
The idea is we're creating a new environment (or installation) for the project, we give it a linux user,
a project name (to be retrieved from the manifest), an environment type, we pass it the --checkout and --pull-db
flags, which will traverse a list of (development, staging, production) upwards.
"""
opt_parser = OptionParser()
opt_parser.add_option("-u", "--user",     dest="username",                      help="System username to associate the environment with.")
opt_parser.add_option("-p", "--project",  dest="project",                       help="Project to use from the manifest, also for credentials.")
opt_parser.add_option("-t", "--type",     dest="env_type",                      help="Type of environment, must be: development, staging, or production")
opt_parser.add_option("-c", "--checkout", dest="checkout", action="store_true", help="Pass to do a git/svn checkout of the repositories defined in the project definition.")
opt_parser.add_option("-d", "--pull-db",  dest="pull_db", action="store_true",  help="Pulls the database from the next highest environment.")

# @todo - add installer flag to run an installer on the created environment

(options, args) = opt_parser.parse_args()

username = options.username
project  = options.project
env_type = options.env_type

if not user_exists(username):
    proceed = prompt("User %s doesn't exist, create and proceed?: " % username, default="y")
    
    if proceed is not 'y':
        print "Aborting."
        import sys
        sys.exit()
    else:
        user = user_utility('/home/dlamanna/app/server_config.json')
        import getpass
        new_user_pass = getpass.getpass("Users Password: ")
        user.add_user(username, new_user_pass)

if not project_exists_in_manifest(project):
    print "Project does not exist in manifest, try creating it first."
    import sys
    sys.exit()

env = environment(username, project, env_type)
env.create()

if options.checkout:
    env.checkout()

if options.pull_db:
    env.pull_db()
