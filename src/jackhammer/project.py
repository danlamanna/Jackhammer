from jackhammer.utils import server
from jackhammer.utils.server import *

from jackhammer.project import project

from fabric.operations import local, prompt

from optparse import OptionParser

import json

# python project.py create_project proj_name
def create_project(slug):
    new_project = project.project(slug)

    project_attrs = {}

    project_attrs['type'] = prompt("Project Type: ", validate=validate_type_field)

def validate_type_field(val):
    valid_types = ['wordpress', 'magento', 'ci']

    try:
        valid_types.index(val)
        return val
    except ValueError:
        raise Exception("Project must be of type wordpress, magento, or ci")

if __name__ == '__main__':
    create_project('tests')
