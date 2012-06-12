from distutils.sysconfig import get_python_lib
from fabric.operations import local

def get_server_config():
    return open('/etc/jackhammer/server_config.json')

def extract_archive(archive, dest="."):
    extract_command = None
    
    if (archive.endswith(".tar.gz") or archive.endswith(".tgz")):
        extract_command = "tar -zxf %(archive)s -C %(dest)s"
    elif (archive.endswith(".zip")):
        extract_command = "unzip %(archive)s -d %(dest)s"
    elif (archive.endswith(".tar.bz2")):
        extract_command = "tar -xjf %(archive)s -C %(dest)s"    
    elif (archive.endswith(".tar")):
        extract_command = "tar -xf %(archive)s -C %(dest)s"

    if extract_command is None:
        return False
    else:
        return local(extract_command % { "archive": archive,
                                         "dest":    dest })

def getpass_validate_regexp(prompt_message, regexp):
    from getpass import getpass
    import re

    # make regexp a compiled pattern
    regexp = regexp if type(regexp) != "str" else re.compile(regexp)

    pass_prompt = getpass(prompt_message)

    if re.match(regexp, pass_prompt):
        return pass_prompt
    else:
        return getpass_validate_regexp(prompt_message, regexp)

def _has_mysqldb_module():
    try:
        import MySQLdb        
    except ImportError:
        return False
    else:
        return True

# Return true/false for good/bad connection info, None if it can't be tested
def _test_mysql_connection(db_name, username, password, db_host):
    if _has_mysqldb_module():
        import MySQLdb

        try:
            MySQLdb.connect(host=db_host,
                            user=username,
                            db=db_name,
                            passwd=password)

            return True
        except:
            return False
    else:
        return None
