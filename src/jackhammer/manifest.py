import json

import pymongo
from pymongo import Connection

conn     = Connection('localhost', 27017)
db       = conn.jackhammer
projects = db.projects

def get_project_manifest():
    project_manifest = []
    
    return [ project_manifest.append(project) for project in projects.find() ]

def get_project(args={}):
    return projects.find_one(args)

def get_count_from_manifest(args={}):
    return projects.find(args).count()

def project_exists(slug):
    return bool(get_count_from_manifest({ "slug": slug }))
