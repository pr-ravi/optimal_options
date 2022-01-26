import argparse

def get_arguments():
    """
    Exposes the needed arguments for the oo command line utility
    """

    parser = argparse.ArgumentParser(description="Run the OO utility")

    # DB actions
    parser.add_argument(
        '--db',
        required=False,
        dest='db_cmd',
        metavar='action',
        help='DB actions'
    )

    return parser.parse_args()