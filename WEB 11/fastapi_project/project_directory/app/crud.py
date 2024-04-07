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

# Маршрут для отримання токена доступу
@app.post("/token/", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Операція, яка дозволяє користувачу переглядати свої дані
@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: TokenData = Depends(get_current_active_user), db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, current_user.email)
    return user



