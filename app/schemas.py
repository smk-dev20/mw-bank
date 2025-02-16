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


class APIResponse(BaseModel):
    message: str
    data: Any

    class Config:
        arbitrary_types_allowed = True