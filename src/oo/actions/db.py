from ast import arg
import logging
import sys
from oo.platforms.nse import loader as nse_loader

__cmd_mapping__ = {
    'nse': nse_loader
}

__method_mapping__ = {
    'load-history': 'load_platform_history',
    'update-history': 'update_platform_history',
    'load-instruments': 'load_instrument_list'
}

def throw_cmd_error(cmd):
    raise Exception(f"Command {cmd} not found")

def process():
    if sys.argv[2] in __method_mapping__:
        method = __method_mapping__[sys.argv[2]]

        cmd = __cmd_mapping__[sys.argv[3]]

        print(cmd)
        print(method)
        if hasattr(cmd, method):
            getattr(cmd, method)()
        else:
            throw_cmd_error(sys.argv[3])
    else:
        throw_cmd_error(sys.argv[2])