from sqlalchemy.orm import Session
import models, schemas, utils
import uuid

#  Create a new customer
def create_customer(db: Session, customer: schemas.CustomerCreate):
    unique_customer_id = utils.generate_unique_id(models.Customer, db)
    
    # Creating a new customer instance
    db_customer = models.Customer(
        customer_id=unique_customer_id,
        customer_first_name=customer.customer_first_name,
        customer_last_name=customer.customer_last_name,
        customer_address=customer.customer_address,
        customer_city=customer.customer_city,
        customer_state=customer.customer_state,
        customer_zipcode=customer.customer_zipcode,
        customer_email=customer.customer_email,
    )

    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)

    customer_response = schemas.CustomerResponse.from_orm(db_customer)
    
    return {"message": "Customer created successfully", "data": customer_response}


# Create a new account
def create_account(db: Session, account: schemas.AccountCreate):
    unique_account_id = utils.generate_unique_id(models.Account, db)
    
    # Creating a new account instance
    db_account = models.Account(
        account_id=unique_account_id,
        customer_id=account.customer_id,  
        account_balance=account.account_balance,  
    )

    db.add(db_account)
    db.commit()
    db.refresh(db_account)

    account_response = schemas.AccountResponse.from_orm(db_account)
    
    return {"message": "Account created successfully", "data": account_response}

# Perform a money transfer
def transfer_money(db: Session, transfer: schemas.TransferCreate):
    sender = db.query(models.Account).filter(models.Account.account_id == transfer.sender_account_id).first()
    receiver = db.query(models.Account).filter(models.Account.account_id == transfer.receiver_account_id).first()

    if not sender or not receiver:
        return {"message": "Error: Invalid accounts", "data": None}  # Error: Invalid accounts

    if sender.account_balance < transfer.amount:
        return {"message": "Error: Insufficient balance", "data": None}  # Error: Insufficient balance
    
    # Generate unique UUID for transfer
    transfer_id = str(uuid.uuid4())

    sender.account_balance -= transfer.amount
    receiver.account_balance += transfer.amount

    # Creating the transfer record
    db_transfer = models.TransferHistory(
        transfer_id=transfer_id,
        sender_account_id=transfer.sender_account_id,
        receiver_account_id=transfer.receiver_account_id,
        amount=transfer.amount,
    )

    db.add(db_transfer)
    db.commit()
    db.refresh(db_transfer)

    transfer_response = schemas.TransferResponse.from_orm(db_transfer)
    
    return {"message": "Transfer successful", "data": transfer_response}

# Create auto transfer rule
def create_auto_transfer_rule(db: Session, rule: schemas.AutoTransferRuleCreate):
    """Handles database insertion for auto transfer rule"""
    db_rule = models.AutoTransferRule(
        at_rule_uuid=str(uuid.uuid4()),
        at_rule_type=rule.at_rule_type,
        at_rule_primary_account_number=rule.at_rule_primary_account_number,
        at_rule_threshold=rule.at_rule_threshold,
        at_rule_linked_account_number=rule.at_rule_linked_account_number,
        at_rule_notes=rule.at_rule_notes,
    )
    
    db.add(db_rule)
    db.commit()
    db.refresh(db_rule)

    rule_response = schemas.AutoTransferRuleResponse.from_orm(db_rule)

    return schemas.APIResponse(message="Auto transfer rule created successfully", data=rule_response)