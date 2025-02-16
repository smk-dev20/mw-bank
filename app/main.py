import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, crud
from database import engine, get_db

# Initialize FastAPI app
app = FastAPI()

# Create tables in the database
models.Base.metadata.create_all(bind=engine)

# Customer Endpoints
@app.post("/customers/", response_model=schemas.APIResponse)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    return crud.create_customer(db, customer)


# Account Endpoints
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


@app.get("/")
def start():
    return {"message": "Welcome to MW-bank"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)