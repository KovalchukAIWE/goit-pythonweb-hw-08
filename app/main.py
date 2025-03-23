from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas, crud
from app.database import SessionLocal, engine

# Створення таблиць
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Contact API",
    description="REST API для зберігання та управління контактами",
    version="1.0.0"
)

# Залежність для отримання сесії бази даних
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Ендпоінт для створення контакту
@app.post("/contacts/", response_model=schemas.ContactOut)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    return crud.create_contact(db, contact)

# Ендпоінт для отримання списку контактів з можливістю пошуку
@app.get("/contacts/", response_model=List[schemas.ContactOut])
def read_contacts(
    skip: int = 0,
    limit: int = 100,
    query: str = Query(None, description="Пошук за іменем, прізвищем або email"),
    db: Session = Depends(get_db)
):
    if query:
        contacts = crud.search_contacts(db, query)
    else:
        contacts = crud.get_contacts(db, skip=skip, limit=limit)
    return contacts

# Ендпоінт для отримання одного контакту за ID
@app.get("/contacts/{contact_id}", response_model=schemas.ContactOut)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = crud.get_contact(db, contact_id)
    if not db_contact:
        raise HTTPException(status_code=404, detail="Контакт не знайдено")
    return db_contact

# Ендпоінт для оновлення контакту
@app.put("/contacts/{contact_id}", response_model=schemas.ContactOut)
def update_contact(contact_id: int, contact: schemas.ContactUpdate, db: Session = Depends(get_db)):
    db_contact = crud.update_contact(db, contact_id, contact)
    if not db_contact:
        raise HTTPException(status_code=404, detail="Контакт не знайдено")
    return db_contact

# Ендпоінт для видалення контакту
@app.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = crud.delete_contact(db, contact_id)
    if not db_contact:
        raise HTTPException(status_code=404, detail="Контакт не знайдено")
    return {"detail": "Контакт видалено"}

# Ендпоінт для отримання контактів з майбутніми днями народження (наступні 7 днів)
@app.get("/contacts/birthdays/", response_model=List[schemas.ContactOut])
def read_birthdays(days: int = 7, db: Session = Depends(get_db)):
    return crud.get_birthdays(db, days)
