#!/usr/bin/python

import sys
from argparse import ArgumentParser, ArgumentError

from commands import Commands


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "branch",
        help=u"a new branch name")
    parser.add_argument(
        "-z", "--host",
        required=True,
        help=u"an original database host")
    parser.add_argument(
        "-p", "--port",
        type=int, default=5432, help=u"an original database port")
    parser.add_argument(
        "-d", "--db",
        required=True,
        help=u"an original database name")
    parser.add_argument(
        "-u", "--owner",
        required=True,
        help=u"an original database owner")
    parser.add_argument(
        "-Z", "--new-host",
        default="127.0.0.1", help=u"a new database host")
    parser.add_argument(
        "-P", "--new-port",
        default=5432, help=u"a new database port")

    try:
        commands = Commands(parser.parse_args())
    except ArgumentError, (e):
        sys.exit(e)

    """Create git-branch and Check whether it's correct"""
    commands.git_create_branch()

    """Export and import database"""
    commands.psql_dump()
    commands.psql_createuser()
    commands.psql_createdb()
    commands.psql_import()

if __name__ == "__main__":
    main()
