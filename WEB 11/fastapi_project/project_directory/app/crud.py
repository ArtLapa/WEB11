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

