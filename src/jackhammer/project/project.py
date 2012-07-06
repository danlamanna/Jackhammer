from jackhammer.manifest import get_project_manifest
from jackhammer.utils.server import get_server_config

from fabric.operations import prompt, local

import json

class project:

    slug = None

    server_config = None

    def __init__(self, slug):
        self.slug = slug
        self.server_config = json.load(get_server_config())

    def _project_exists(self):
        if self.slug != None:
            if self.slug in get_project_manifest()['projects']:
                return True
            else:
                return False
        else:
            raise Exception("No slug set on project object.")

    def create_project(self, attributes_dict):
        if self._project_exists():
            return False
        else:
            project_manifest = get_project_manifest()

            project_manifest['projects'][self.slug] = attributes_dict
            json.dump(project_manifest, open(self.server_config["project_manifest"], "w+"), indent=4)
            
def get_project_environment(project_slug, env_type):
    try:
        return get_project_manifest()["projects"][project_slug]["environments"][env_type]
    except:
        return False
        
        
