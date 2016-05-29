import logging
from contextlib import contextmanager

import pkg_resources
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#from akk.db.entities import Base

_logger = logging.getLogger("db")

def _get_engine():
    db_file_name = pkg_resources.resource_filename("akk", "db_data/database.db")
    _logger.debug("Opening database file at {db_file_name}.".format(db_file_name=db_file_name))
    engine = create_engine('sqlite:///{db_file_name}'.format(db_file_name=db_file_name))

    #if autofill:
    #    _logger.debug("Creating tables in database.")
    #    Base.metadata.create_all(engine)

    return engine

SessionMaker = sessionmaker(bind=_get_engine())

@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = SessionMaker()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()