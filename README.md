# mw-bank
This is a FastAPI-based banking application that provides basic operations for customers, accounts, and transfer history using PostgreSQL as the database.

## Features
- Create and manage customers
- Open and manage accounts
- Perform money transfers between accounts
- Retrieve account balance and transfer history
- Secure and efficient database operations using SQLAlchemy

## Prerequisites
Ensure you have the following installed:
- Python 3.8+
- PostgreSQL
- `pip` (Python package manager)

## Installation

### 1. Clone the repository
```sh
git clone https://github.com/smk-dev20/mw-bank.git
cd mw-bank
```
### 2. Dev Environment Setup
#### Setup a virtual environment - Unix/Linux
```
python3 -m venv .venv
source .venv/bin/activate
```

#### Setup a virtual environment - Windows - Command Prompt
```
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies
```
pip install -r requirements.txt
```

### 4. Setup Environment Variables
Create a .env file and configure database credentials:
```
DB_USER=myuser
DB_PASSWORD=mypassword
DB_HOST=localhost
DB_PORT=5432
DB_NAME=mydatabase
```

### 5. Run the application
```
python app/main.py
```

Application will start on http://localhost:8000

## APIS

### 1. Create Customer
```
URL: http://127.0.0.1:8000/customers
Method: POST
Header: Content-Type: application/json
Body:
{
    "customer_first_name": "Greg",
    "customer_last_name": "House",
    "customer_address": "123 North Ave",
    "customer_city": "Anycity",
    "customer_state": "NJ",
    "customer_zipcode": 23455,
    "customer_email": "ghouse@ppth.org"
}
Expected Response:
{
    "message": "Customer created successfully",
    "data": {
        "customer_first_name": "Greg",
        "customer_last_name": "House",
        "customer_address": "123 North Ave",
        "customer_city": "Anycity",
        "customer_state": "NJ",
        "customer_zipcode": 23455,
        "customer_email": "ghouse@ppth.org",
        "customer_id": 214923,
        "created_on": "2025-02-16T11:44:28.558521",
        "updated_on": "2025-02-16T11:44:28.558521"
    }
}
```

### 2. Create Account
```
URL: http://127.0.0.1:8000/accounts
Method: POST 
Header: Content-Type: application/json
Body:
{
    "customer_id": 214923,
    "account_balance": 5000
}

Expected Response:
{
    "message": "Account created successfully",
    "data": {
        "customer_id": 214923,
        "account_balance": 5000.0,
        "account_id": 528981,
        "created_on": "2025-02-16T11:54:09.133810",
        "updated_on": "2025-02-16T11:54:09.133810"
    }
}
```

### 3. Get Account Balance by Account ID
```
URL: http://127.0.0.1:8000/accounts/528981/balance
Method: GET
Body: None
Expected Response:
{
    "account_id": 528981,
    "balance": 5000.0
}
```

### 4. Transfer Funds
```
URL: http://127.0.0.1:8000/transfer
Method: POST
Header: Content-Type: application/json
Body:
{
    "sender_account_id": 528981,
    "receiver_account_id": 907675,
    "amount": 1000.00
}
Expected Response:
{
    "message": "Transfer successful",
    "data": {
        "sender_account_id": 528981,
        "receiver_account_id": 907675,
        "amount": 1000.0,
        "transfer_id": "f1d7af0b-f1fe-4546-8c63-e2df4a800ae2",
        "transfer_time": "2025-02-16T11:59:00.900862"
    }
}
```

### 5. Get Transfer History by Account ID
```
URL: http://127.0.0.1:8000/accounts/528981/transfers
Method: GET
Body: None
Expected Response:
{
    "account_id": 528981,
    "transfers": [
        {
            "transfer_id": "f1d7af0b-f1fe-4546-8c63-e2df4a800ae2",
            "type": "sent",
            "to": 907675,
            "amount": 1000.0,
            "date": "2025-02-16T11:59:00.900862"
        }
    ],
    "current_balance": 4000.0
}
```
### 6. Create Auto Transfer Rule
```
URL: http://127.0.0.1:8000/create-auto-transfer-rule
Method: POST
Header: Content-Type: application/json
Body:
{
    "at_rule_type": "TARGET_BALANCE",
    "at_rule_primary_account_number": 928113,
    "at_rule_threshold": 5000.0,
    "at_rule_linked_account_number": 148160,
    "at_rule_notes": "Target balance rule for account 928113"
}

Expected Response:
{
    "message": "Auto transfer rule created successfully",
    "data": {
        "at_rule_type": "TARGET_BALANCE",
        "at_rule_primary_account_number": 928113,
        "at_rule_threshold": 5000.0,
        "at_rule_linked_account_number": 148160,
        "at_rule_notes": "Target balance rule for account 928113",
        "at_rule_uuid": "8cd93ac4-dfa6-4f17-84e8-d8ee37ba2e57",
        "created_on": "2025-02-16T14:52:13.902006",
        "updated_on": "2025-02-16T14:52:13.902006"
    }
}

#Note: ZERO_BALANCE is the other rule_type for which rule_threshold should be 0.0
```

### 7. Execute Auto Transfer Rules
Note: This API can be setup to be invoked via a cronjob/event trigger (TBD)
```
URL: http://127.0.0.1:8000/execute-auto-transfer-rules
Method: GET
Body: None
Expected Response:
{
    "message": "Auto transfer execution completed",
    "data": [
        {
            "rule_id": "00fe4af6-cfd6-41ce-8b78-327f56975e8c",
            "status": "Transfer successful"
        },
        {
            "rule_id": "8cd93ac4-dfa6-4f17-84e8-d8ee37ba2e57",
            "status": "Transfer successful"
        }
    ]
}
```