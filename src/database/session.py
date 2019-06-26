from contextlib import contextmanager

from sqlalchemy.orm import sessionmaker

from src.database.base import DATABASE, create_engine, Base


@contextmanager
def session_context(new_engine=False):
    if new_engine:
        engine = create_engine()
        Base.prepare(engine)
    else:
        engine = DATABASE
    session = sessionmaker(engine)()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def session_scope_func(func):
    def wrapped(*args, **kwargs):
        session = sessionmaker(DATABASE)()
        try:
            res = func(session, *args, **kwargs)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return res

    return wrapped


def session_scope_method(func):
    def wrapped(self=None, *args, **kwargs):
        session = sessionmaker(DATABASE)()
        try:
            res = func(self, session, *args, **kwargs)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return res

    return wrapped
