from sqlalchemy import create_engine as base_create_engine
from sqlalchemy.ext.automap import automap_base

import settings


def create_engine():
    return base_create_engine(settings.DB_URL)


DATABASE = create_engine()
Base = automap_base(bind=DATABASE)
