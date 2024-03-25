# crud.py

from sqlalchemy.orm import Session
from . import models

# Додамо функцію для пошуку контактів за ім'ям, прізвищем або адресою електронної пошти
def search_contacts(db: Session, query: str):
    return db.query(models.Contact).filter(
        (models.Contact.first_name.ilike(f"%{query}%")) |
        (models.Contact.last_name.ilike(f"%{query}%")) |
        (models.Contact.email.ilike(f"%{query}%"))
    ).all()


# crud.py

from sqlalchemy.orm import Session
from datetime import date, timedelta
from . import models

# Додамо функцію для отримання контактів з найближчими днями народження
def get_contacts_with_birthdays(db: Session, days: int = 7):
    today = date.today()
    end_date = today + timedelta(days=days)
    return db.query(models.Contact).filter(
        (models.Contact.birthday >= today) & (models.Contact.birthday <= end_date)
    ).all()

# crud.py

from sqlalchemy.orm import Session
from . import models

def create_contact(db: Session, contact_data: dict):
    db_contact = models.Contact(**contact_data)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def get_contacts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Contact).offset(skip).limit(limit).all()

def get_contact(db: Session, contact_id: int):
    return db.query(models.Contact).filter(models.Contact.id == contact_id).first()

def update_contact(db: Session, contact_id: int, contact_data: dict):
    db_contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    for key, value in contact_data.items():
        setattr(db_contact, key, value)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def delete_contact(db: Session, contact_id: int):
    db_contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    db.delete(db_contact)
    db.commit()


