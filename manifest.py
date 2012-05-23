import json

def get_project_manifest():
    manifest = open('/home/dlamanna/app/etc/manifests/projects.json').read()

    return json.loads(manifest if manifest != '' else '{ "projects": {} }')
