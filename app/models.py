from sqlalchemy import Column, String, Numeric, DateTime, Enum, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class Wallet(Base):
    __tablename__ = "wallets"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    balance = Column(Numeric(scale=2), nullable=False, default=0)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class Operation(Base):
    __tablename__ = "operations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    wallet_id = Column(UUID(as_uuid=True), nullable=False)
    operation_type = Column(Enum('DEPOSIT', 'WITHDRAW', name='operation_type'), nullable=False)
    amount = Column(Numeric(scale=2), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
