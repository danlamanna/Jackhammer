"""
Replacement for ${string}
"""
import re
from fabric.operations import local
from fabric.api import *
def burst_replace(string, replacement, text):
    from fabric.operations import local
    return local("sed 's/" + re.escape(string) + '/' + re.escape(replacement) + '/g ' + text)
