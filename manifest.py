import json

def get_project_manifest():
    manifest = open('/home/dlamanna/projects.json').read()

    return json.loads(manifest if manifest != '' else '{ "projects": {} }')
