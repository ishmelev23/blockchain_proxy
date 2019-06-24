import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from src.database import Base


class Transaction(Base):

    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    blocknumber = Column(Integer, nullable=True, default=None)
    trx_hash = Column(String(64), unique=True)
    published = Column(Boolean, default=False)
    updated = Column(DateTime, default=datetime.datetime.utcnow)
    created = Column(DateTime, default=datetime.datetime.utcnow)

    @property
    def is_pending(self):
        return self.blocknumber is None

    @property
    def dict(self):
        return {
            'id': self.id,
            'blocknumber': self.blocknumber,
            'trx_hash': self.trx_hash,
            'published': self.published,
            'updated': self.updated.timestamp(),
            'created': self.created.timestamp()
        }

    def __repr__(self):
        return '<Transaction %s >' % self.trx_hash
