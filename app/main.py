import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, crud
from database import engine, get_db

# Initialize FastAPI app
app = FastAPI()

# Create tables in the database
models.Base.metadata.create_all(bind=engine)

# Customer Endpoint
@app.post("/customers/", response_model=schemas.APIResponse)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    return crud.create_customer(db, customer)


# Account Endpoint
@app.post("/accounts/", response_model=schemas.APIResponse)
def create_account(account: schemas.AccountCreate, db: Session = Depends(get_db)):
    customer = db.query(models.Customer).filter(models.Customer.customer_id == account.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    return crud.create_account(db, account)

# Transfer Endpoint
@app.post("/transfer/", response_model=schemas.APIResponse)
def transfer_money(transfer: schemas.TransferCreate, db: Session = Depends(get_db)):
    transaction = crud.transfer_money(db, transfer)
    if transaction is None:
        raise HTTPException(status_code=400, detail="Transfer failed: Invalid accounts or insufficient balance")
    return transaction

# Get Balance for given account
@app.get("/accounts/{account_id}/balance")
def get_account_balance(account_id: int, db: Session = Depends(get_db)):
    account = db.query(models.Account).filter(models.Account.account_id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"account_id": account_id, "balance": account.account_balance}

# Get Transfer history for given account
@app.get("/accounts/{account_id}/transfers")
def get_transfer_history(account_id: int, db: Session = Depends(get_db)):
    # Fetch account details
    account = db.query(models.Account).filter(models.Account.account_id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    transfers_sent = db.query(models.TransferHistory).filter(models.TransferHistory.sender_account_id == account_id).all()
    transfers_received = db.query(models.TransferHistory).filter(models.TransferHistory.receiver_account_id == account_id).all()

    transfer_history = [
        {"transfer_id": t.transfer_id, "type": "sent", "to": t.receiver_account_id, "amount": t.amount, "date": t.transfer_time}
        for t in transfers_sent
    ] + [
        {"transfer_id": t.transfer_id, "type": "received", "from": t.sender_account_id, "amount": t.amount, "date": t.transfer_time}
        for t in transfers_received
    ]

    # Sort transactions chronologically by transfer_time
    transfer_history.sort(key=lambda x: x["date"])

    current_balance = account.account_balance  

    return {"account_id": account_id, "transfers": transfer_history, "current_balance": current_balance}

# Create Transfer Rule
@app.post("/create_auto_transfer_rule/", response_model=schemas.APIResponse)
def create_auto_transfer_rule(rule: schemas.AutoTransferRuleCreate, db: Session = Depends(get_db)):
    # Validate at_rule_type and at_rule_threshold
    if rule.at_rule_type not in {"ZERO_BALANCE", "TARGET_BALANCE"}:
        raise HTTPException(status_code=400, detail="Invalid at_rule_type. Must be 'ZERO_BALANCE' or 'TARGET_BALANCE'.")
    
    if rule.at_rule_type == "ZERO_BALANCE" and rule.at_rule_threshold != 0:
        raise HTTPException(status_code=400, detail="For ZERO_BALANCE type, at_rule_threshold must be 0.")
    
    if rule.at_rule_type == "TARGET_BALANCE" and rule.at_rule_threshold == 0:
        raise HTTPException(status_code=400, detail="For TARGET_BALANCE type, at_rule_threshold must be non-zero.")

    # Validate if primary and linked account numbers exist
    primary_account = db.query(models.Account).filter(models.Account.account_id == rule.at_rule_primary_account_number).first()
    linked_account = db.query(models.Account).filter(models.Account.account_id == rule.at_rule_linked_account_number).first()
    
    if not primary_account:
        raise HTTPException(status_code=400, detail="Primary account does not exist.")
    
    if not linked_account:
        raise HTTPException(status_code=400, detail="Linked account does not exist.")

    return crud.create_auto_transfer_rule(db,rule)

# Execute Transfer Rules
@app.get("/execute_auto_transfer_rules", response_model=schemas.APIResponse)
def execute_auto_transfer_rules(db: Session = Depends(get_db)):
    """Executes auto transfer rules and processes account transfers accordingly"""
    
    # Fetch all active auto transfer rules
    rules = db.query(models.AutoTransferRule).all()
    
    if not rules:
        return {"message": "No auto transfer rules found", "data": None}
    
    results = []
    
    for rule in rules:
        primary_account = db.query(models.Account).filter(models.Account.account_id == rule.at_rule_primary_account_number).first()
        linked_account = db.query(models.Account).filter(models.Account.account_id == rule.at_rule_linked_account_number).first()

        if not primary_account or not linked_account:
            print(f"Skipping rule {rule.at_rule_uuid}: Invalid account(s)")
            results.append({"rule_id": rule.at_rule_uuid, "status": "skipped", "reason": "Invalid account(s)"})
            continue

        print(f"------Processing rule {rule.at_rule_uuid}: Type={rule.at_rule_type}------")

        if rule.at_rule_type == "ZERO_BALANCE":
            # If primary account has balance > 0, transfer all funds to linked account
            if primary_account.account_balance > rule.at_rule_threshold:
                amount_to_transfer = primary_account.account_balance
                transfer_data = schemas.TransferCreate(
                    sender_account_id=primary_account.account_id,
                    receiver_account_id=linked_account.account_id,
                    amount=amount_to_transfer
                )
                transfer_result = crud.transfer_money(db, transfer_data)
                print(f"ZERO_BALANCE Rule Applied: Transferred {amount_to_transfer} from {primary_account.account_id} to {linked_account.account_id}")
            else:
                print(f"Skipping ZERO_BALANCE rule {rule.at_rule_uuid}: No funds to transfer")
                transfer_result = {"message": "No funds to transfer", "data": None}

        elif rule.at_rule_type == "TARGET_BALANCE":
            # If primary account balance is below the threshold, transfer necessary amount from linked account
            balance_deficit = rule.at_rule_threshold - primary_account.account_balance

            if balance_deficit > 0 and linked_account.account_balance >= balance_deficit:
                transfer_data = schemas.TransferCreate(
                    sender_account_id=linked_account.account_id,
                    receiver_account_id=primary_account.account_id,
                    amount=balance_deficit
                )
                transfer_result = crud.transfer_money(db, transfer_data)
                print(f"TARGET_BALANCE Rule Applied: Transferred {balance_deficit} from {linked_account.account_id} to {primary_account.account_id}")
            else:
                print(f"Skipping TARGET_BALANCE rule {rule.at_rule_uuid}: Insufficient linked account balance or no deficit")
                transfer_result = {"message": "Insufficient linked account balance or no deficit", "data": None}
        
        results.append({"rule_id": rule.at_rule_uuid, "status": transfer_result["message"]})

    return {"message": "Auto transfer execution completed", "data": results}

@app.get("/")
def start():
    return {"message": "Welcome to MW-bank"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)