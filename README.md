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