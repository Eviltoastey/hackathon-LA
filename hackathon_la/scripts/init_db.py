"""
Initializes the database with the tables.
"""
import os
import sys

from pyramid.paster import setup_logging, get_appsettings
from pyramid.scripts.common import parse_vars

from hackathon_la.model import get_engine
from hackathon_la.model.models import *


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    engine = get_engine(settings)
    Base.metadata.create_all(engine)