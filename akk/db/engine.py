from contextlib import contextmanager

from akk import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from akk.db.entities import Base
from flask import g


def _get_engine():
    db_file_name = app.config["DATABASE"]
    engine = create_engine('sqlite:///{db_file_name}'.format(db_file_name=db_file_name))

    return engine


def init_db():
    Base.metadata.create_all(get_engine())


def get_engine():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = _get_engine()
    return g.sqlite_db


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""

    if not hasattr(g, 'sqlite_session_maker'):
        g.sqlite_session_maker = sessionmaker(bind=get_engine())

    SessionMaker = g.sqlite_session_maker

    session = SessionMaker()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


