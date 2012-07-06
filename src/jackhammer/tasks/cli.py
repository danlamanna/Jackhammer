from jackhammer.utils.user import user_exists, user_utility
from jackhammer.project.project import project_exists_in_manifest

def create_env(args):
    if not project_exists_in_manifest(args.project):
        print "Project doesn't exist in manifest, nothing to do here."
        
        import sys
        sys.exit()
        
        env = environment(args.user, args.project, args.type, args.url)
    
        env_results = env.create()
        
        # implement with-package, pull-db, checkout
        
        print "Creating env the right way."
    else:
        print "Project doesn't exist in manifest, nothing to do."

def remove_env(args):
    if not project_exists_in_manifest(args.project):
        print "Project doesn't exist in manifest, nothing to do."
        
        import sys
        sys.exit()
    else:
        env = environment(args.user, args.project, args.type)
        
        preserve_db = True if args.preserve_db else False
        
        env.remove(args.preserve_db)
        
    print "Removing env"

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
