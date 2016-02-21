import logging

import pkg_resources
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from akk.db.entities import Base

_logger = logging.getLogger("db")


def get_engine(autofill=True):
    db_file_name = pkg_resources.resource_filename("akk", "db_data/database.db")
    _logger.debug("Opening database file at {db_file_name}.".format(db_file_name=db_file_name))
    engine = create_engine('sqlite:///{db_file_name}'.format(db_file_name=db_file_name))

    if autofill:
        _logger.debug("Creating tables in database.")
        Base.metadata.create_all(engine)

    return engine


def get_session():
    engine = get_engine()
    SessionMaker = sessionmaker()
    SessionMaker.configure(bind=engine)

    session = SessionMaker()
    return session
