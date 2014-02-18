## KIWI brancher

KIWI brancher is a command line tool which can create a new git branch and copy a new postgres database from original one.
You will use this tool, for example, when you want to automatically make your development environment same as production in each git branch.

### Version

0.1

### Requirements

* python 2.7+
* pip
* git
* postgresql

### Dependencies

None


## Usage

    $ kiwibrancher feature/task -z 11.11.11.0 -d orig_dbname -u orig_dbowner

As you execute KIWI brancher like above, a new branch `feature/task` and a new database `feature_task` are created.


## License

MPL2 license, see LICENSE file.
