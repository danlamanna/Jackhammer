"""
Replacement for ${string}
"""
import re
from fabric.operations import local
from fabric.api import *

def jh_replace(string, replacement, text):
    if replacement is None:
        replacement = ""
        
    return text.replace("${%s}" % str(string), replacement)
