import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from src.database.base import Base


class Transaction(Base):

    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    blocknumber = Column(Integer, nullable=True, default=None)
    blockhash = Column(String(66), nullable=True, default=None)
    trx_hash = Column(String(66), unique=True)
    contract_name = Column(String(255))
    func_name = Column(String(255))
    data = Column(String(2048))
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
            'contract_name': self.contract_name,
            'func_name': self.func_name,
            'data': self.data,
            'updated': self.updated.timestamp(),
            'created': self.created.timestamp()
        }

    def __repr__(self):
        return '<Transaction %s >' % self.trx_hash
