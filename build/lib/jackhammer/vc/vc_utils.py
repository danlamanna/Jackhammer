
from subprocess import call

import ipdb; ipdb.set_trace()
call('svn status .')


class vc_utils:

    def commit(self):
        if (_is_git_repo()):
            return _git_commit()
        elif (_is_svn_repo()):
            return _svn_commit()

        return False
        
    def _git_commit(self):
        return local('git commit')

    def _svn_commit(self):
        return local('svn commit')

    def _is_git_repo(self):
        return False

    def _is_svn_repo(self):
        return not bool('not a working copy' in local('svn status'))
