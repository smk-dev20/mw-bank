from pydantic import BaseModel
from datetime import datetime
from typing import Any

# Customer Schema
class CustomerBase(BaseModel):
    customer_first_name: str
    customer_last_name: str
    customer_address: str
    customer_city: str
    customer_state: str
    customer_zipcode: int
    customer_email: str

class CustomerCreate(CustomerBase):
    pass

class CustomerResponse(CustomerBase):
    customer_id: int
    created_on: datetime
    updated_on: datetime
    
    class Config:
        from_attributes = True

# Account Schema
class AccountBase(BaseModel):
    customer_id: int
    account_balance: float

class AccountCreate(AccountBase):
    pass

class AccountResponse(AccountBase):
    account_id: int
    created_on: datetime
    updated_on: datetime
    
    class Config:
        from_attributes = True

# Transfer Schema
class TransferBase(BaseModel):
    sender_account_id: int
    receiver_account_id: int
    amount: float

class TransferCreate(TransferBase):
    pass

class TransferResponse(TransferBase):
    transfer_id: str
    transfer_time: datetime
    class Config:
        from_attributes = True

# Auto-transfer Rule Schema
from pydantic import BaseModel
from datetime import datetime
import uuid

class AutoTransferRuleBase(BaseModel):
    at_rule_type: str
    at_rule_primary_account_number: int
    at_rule_threshold: float
    at_rule_linked_account_number: int
    at_rule_notes: str

class AutoTransferRuleCreate(AutoTransferRuleBase):
    pass

class AutoTransferRuleResponse(AutoTransferRuleBase):
    at_rule_uuid: str
    created_on: datetime
    updated_on: datetime

    class Config:
        from_attributes = True

class APIResponse(BaseModel):
    message: str
    data: Any

    class Config:
        arbitrary_types_allowed = True