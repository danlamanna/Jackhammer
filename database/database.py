from fabric.api import *
from fabric.operations import local

class database_dump:

    sql = None
    
    def __init__(self, sql):
        self.sql = sql

    def find_replace(self, find, replace):
        self.sql = self.sql.replace(find, replace)

        return self

    def export_to(self, filepath):
        fh = open(filepath)

        fh.write(self.sql)
        fh.close()

        return self

    def import_into(self, db_user, db_pass, db_name, db_host="localhost"):
        import re
        
        return local("mysql -u%(db_user)s -p%(db_pass)s --host=\"%(db_host)s\" %(db_name)s < %(sql_query)s" % {
            "db_user": db_user,
            "db_pass": re.escape(db_pass),
            "db_name": db_name,
            "db_host": db_host,
            "sql_query": self.sql })
