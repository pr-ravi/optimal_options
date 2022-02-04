import sys
import oo.actions.db as db
import oo.actions.build as build

def parse():
    if sys.argv[1] == 'db':
        db.process()
    elif sys.argv[1] == 'build':
        build.process()
    else:
        raise Exception("argument wrong")