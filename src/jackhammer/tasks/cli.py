from jackhammer.utils.user import user_exists, user_utility
from jackhammer.manifest import project_exists

from jackhammer.environment.environment import *

def create_env(args):
    if not project_exists(args.project):
        print "Project doesn't exist in manifest, nothing to do here."
        
        import sys
        sys.exit()
    else:
        env = environment(args.user, args.project, args.type, args.url)
    
        env_results = env.create()

        if args.checkout:
            env.checkout()        
        
        # @todo implement with-package, pull-db

def remove_env(args):
    if not project_exists(args.project):
        print "Project doesn't exist in manifest, nothing to do."
        
        import sys
        sys.exit()
    else:
        env = environment(args.user, args.project, args.type)
        
        preserve_db = True if args.preserve_db else False
        
        env.remove(args.preserve_db)
        
    return True

def create_user_if_not_exists(user):
    if not user_exists(user):
        proceed = prompt("User %s doesn't exist, create and proceed?: " % user, default="y")

        if proceed is not "y":
            print "Aborting"
            import sys
            sys.exit()
        else:
            user = user_utility('/etc/jackhammer/server_config.json')
            
            from getpass import getpass
            user.add_user(user, getpass("Users Password: "))
            
            print "User %s created." % user
