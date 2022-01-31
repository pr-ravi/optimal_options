import sys
import oo.actions.db as db

def parse():
    if sys.argv[1] == 'db':
        db.process()