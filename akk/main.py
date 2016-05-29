#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""
import argparse
import logging
import sys

from akk import __version__
from akk.db.engine import session_scope
from akk.db.entities import Dance
from akk.flask_application import _app

__author__ = "Nils"
__copyright__ = "Nils"
__license__ = "none"

_logger = logging.getLogger(__name__)


def parse_args(args):
    """
    Parse command line parameters

    :param args: command line parameters as list of strings
    :return: command line parameters as :obj:`argparse.Namespace`
    """
    parser = argparse.ArgumentParser(
        description="Just a Hello World demonstration")
    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version='akk {ver}'.format(ver=__version__))
    return parser.parse_args(args)


def main(args):
    args = parse_args(args)

    with session_scope() as s:
        for dance in s.query(Dance).all():
            s.delete(dance)

    with session_scope() as s:
        tango = Dance(name="Tango")
        s.add(tango)
        tango = Dance(name="Test")
        s.add(tango)

    _app.run(debug=False)
    _logger.info("Script ends here")


def run():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
