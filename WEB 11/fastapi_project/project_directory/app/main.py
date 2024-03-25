# main.py

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, world!"}

from . import crud, models, schemas, database

app = FastAPI()

# З'єднання з базою даних
database.Base.metadata.create_all(bind=database.engine)

# Залежність для отримання сесії бази даних
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Операція створення нового контакту
@app.post("/contacts/", response_model=schemas.Contact)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    return crud.create_contact(db=db, contact_data=contact)

# Операція отримання списку всіх контактів
@app.get("/contacts/", response_model=List[schemas.Contact])
def read_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    contacts = crud.get_contacts(db=db, skip=skip, limit=limit)
    return contacts

# Операція отримання контакту за ідентифікатором
@app.get("/contacts/{contact_id}", response_model=schemas.Contact)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = crud.get_contact(db=db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

# Операція оновлення існуючого контакту
@app.put("/contacts/{contact_id}", response_model=schemas.Contact)
def update_contact(contact_id: int, contact: schemas.ContactUpdate, db: Session = Depends(get_db)):
    db_contact = crud.get_contact(db=db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return crud.update_contact(db=db, contact_id=contact_id, contact_data=contact)

# Операція видалення контакту
@app.delete("/contacts/{contact_id}", response_model=schemas.Contact)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = crud.get_contact(db=db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    crud.delete_contact(db=db, contact_id=contact_id)
    return db_contact

# Операція пошуку контактів за ім'ям, прізвищем або адресою електронної пошти
@app.get("/contacts/search/", response_model=List[schemas.Contact])
def search_contacts(query: str, db: Session = Depends(get_db)):
    return crud.search_contacts(db=db, query=query)

# Операція отримання списку контактів з днями народження на найближчі 7 днів
@app.get("/contacts/birthdays/", response_model=List[schemas.Contact])
def contacts_with_birthdays(days: int = 7, db: Session = Depends(get_db)):
    return crud.get_contacts_with_birthdays(db=db, days=days)


