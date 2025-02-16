import random
from sqlalchemy.orm import Session
import models

def generate_unique_id(model, db: Session):
    while True:
        random_id = random.randint(100000, 999999)  # 6-digit random number
        exists = db.query(model).filter(model.customer_id == random_id).first() if model == models.Customer else db.query(model).filter(model.account_id == random_id).first()
        if not exists:
            return random_id