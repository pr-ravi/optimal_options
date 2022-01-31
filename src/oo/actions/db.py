import sys
from oo.platforms.nse import loader as nse_loader

def process():
    if sys.argv[2] == 'load-instruments':
        if sys.argv[3] == 'nse':
            nse_loader.load_instrument_list()
    elif sys.argv[2] == 'load-history':
        if sys.argv[3] == 'nse':
            nse_loader.load_platform_history()