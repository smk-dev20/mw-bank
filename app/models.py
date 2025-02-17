from sqlalchemy import Column, BigInteger, Integer, String, Float, TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
import uuid

# Customers table
class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(BigInteger, primary_key=True, index=True, unique=True)
    customer_first_name = Column(String(255), nullable=False)
    customer_last_name = Column(String(255), nullable=False)
    customer_address = Column(String(255), nullable=False)
    customer_city = Column(String(255), nullable=False)
    customer_state = Column(String(255), nullable=False)
    customer_zipcode = Column(Integer, nullable=False)
    customer_email = Column(String(100), unique=True, nullable=False)

    created_on = Column(TIMESTAMP, nullable=False, default=func.now())  
    updated_on = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.current_timestamp())

    accounts = relationship("Account", back_populates="customer")

# Accounts table
class Account(Base):
    __tablename__ = "accounts"

    account_id = Column(Integer, primary_key=True, index=True, unique=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"), nullable=False)
    account_balance = Column(Float, default=0.0)
    created_on = Column(TIMESTAMP, nullable=False, default=func.now())  
    updated_on = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.current_timestamp())

    customer = relationship("Customer", back_populates="accounts")
    sent_transfers = relationship("TransferHistory", foreign_keys="[TransferHistory.sender_account_id]", back_populates="sender")
    received_transfers = relationship("TransferHistory", foreign_keys="[TransferHistory.receiver_account_id]", back_populates="receiver")

# Transfer History table
class TransferHistory(Base):
    __tablename__ = "transfer_history"

    transfer_id = Column(String, primary_key=True,  unique=True, index=True, default=lambda: str(uuid.uuid4()))
    sender_account_id = Column(Integer, ForeignKey("accounts.account_id"), nullable=False)
    receiver_account_id = Column(Integer, ForeignKey("accounts.account_id"), nullable=False)
    amount = Column(Float, nullable=False)
    transfer_time = Column(TIMESTAMP, server_default=func.now())

    sender = relationship("Account", foreign_keys=[sender_account_id], back_populates="sent_transfers")
    receiver = relationship("Account", foreign_keys=[receiver_account_id], back_populates="received_transfers")

# Auto-transfer Rules table
class AutoTransferRule(Base):
    __tablename__ = "auto_transfer_rules"

    at_rule_uuid = Column(String(255), primary_key=True, unique=True, default=lambda: str(uuid.uuid4()))
    at_rule_type = Column(String(255), nullable=False)
    at_rule_primary_account_number = Column(BigInteger, nullable=False)
    at_rule_threshold = Column(Float, nullable=False)
    at_rule_linked_account_number = Column(BigInteger, nullable=False)
    at_rule_notes = Column(String(255), nullable=False)
    created_on = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_on = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.current_timestamp())