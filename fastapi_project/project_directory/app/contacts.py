# contacts.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models import Contact
from schemas import ContactResponse
from auth_service import get_current_user
from repository_contact import get_contact
from database import get_db

router = APIRouter()

@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(
    contact_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    contact = await get_contact(contact_id, db, current_user)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

from fastapi import APIRouter, Depends, HTTPException
from ratelimit import limits, RateLimitException
from datetime import timedelta

router = APIRouter()

# Ліміт запитів: 100 запитів на хвилину
@limits(calls=100, period=timedelta(minutes=1))
@router.get("/")
async def get_contacts():
    return {"message": "Contacts retrieved successfully"}
    
