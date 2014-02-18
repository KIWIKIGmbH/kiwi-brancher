import sys
from subprocess import check_call, CalledProcessError


class Commands(object):
    class CommandConstants(object):
        """Filenames"""
        TMPDIR = "kiwi_brancher_temporary"

        """Create git-branch"""
        GIT_BRANCH = "git branch %s"

        """Copy postgres database"""
        PSQL_DUMP = "pg_dump -h %s -p %s -U %s %s > %s/dump.sql"
        PSQL_CREATEUSER = "createuser %s"
        PSQL_CREATEDB = "createdb -O %s %s"
        PSQL_IMPORT = "psql -h %s -p %s %s -f %s/dump.sql"

        """Make and remove a temporary directory"""
        MKDIR = 'mkdir %s' % (TMPDIR)
        RMDIR = "rm -r %s" % (TMPDIR)

        """Clean up if an error happens"""
        GIT_BRANCH_DEL = "git branch -d %s"

        PSQL_DROPDB = "dropdb -O %s %s"
        PSQL_DROPUSER = "dropuser %s"

    commands = CommandConstants()
    methods = [
        "git_create_branch", "_mkdir", "psql_createuser", "psql_createdb",
    ]

    def __init__(self, args):
        """a git-branch name"""
        self.branch = args.branch

        """an original database information"""
        self.host = args.host
        self.port = args.port
        self.owner = args.owner
        self.db = args.db

        """a new database information"""
        self.new_owner = '_'.join(self.branch.rsplit('/'))
        self.new_db = self.new_owner
        self.nhost = args.new_host
        self.nport = args.new_port

        self.flags = {}
        for m in self.methods:
            self.flags[m] = False

    def _call(self, command):
        try:
            check_call(
                command, shell=True,
                stderr=sys.stdout, stdout=open("/dev/null", "w"))
        except CalledProcessError, (e):
            self._cleanup(e)

    def _cleanup(self, e):
        if self.flags["psql_createdb"]:
            self._call(self.commands.PSQL_DROPDB % (
                self.new_owner, self.new_db))

        if self.flags["psql_createuser"]:
            self._call(self.commands.PSQL_DROPUSER % (self.new_owner))

        if self.flags["_mkdir"]:
            self._rmdir()

        if self.flags["git_create_branch"]:
            self._call(self.commands.GIT_BRANCH_DEL % (self.branch))

        sys.exit(e)

    def _mkdir(self):
        self._call(self.commands.MKDIR)
        self.flags["_mkdir"] = True

    def _rmdir(self):
        self._call(self.commands.RMDIR)

    def git_create_branch(self):
        self._call(self.commands.GIT_BRANCH % (self.branch))
        self.flags["git_create_branch"] = True

    def psql_dump(self):
        self._mkdir()

        self._call(self.commands.PSQL_DUMP % (
            self.host, self.port, self.owner, self.db, self.commands.TMPDIR))

    def psql_createuser(self):
        self._call(self.commands.PSQL_CREATEUSER % (self.new_owner))
        self.flags["psql_createuser"] = True

    def psql_createdb(self):
        self._call(self.commands.PSQL_CREATEDB % (self.new_owner, self.new_db))
        self.flags["psql_createdb"] = True

    def psql_import(self):
        self._call(self.commands.PSQL_IMPORT % (
            self.nhost, self.nport, self.new_db, self.commands.TMPDIR))

        self._rmdir()
