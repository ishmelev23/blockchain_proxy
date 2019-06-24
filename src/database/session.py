from sqlalchemy.orm import sessionmaker

from src.database.base import DATABASE


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