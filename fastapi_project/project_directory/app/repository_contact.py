# repository_contact.py

async def get_contact(contact_id: int, db: AsyncSession, user: User):
    stmt = select(Contact).filter_by(id=contact_id, user_id=user.id)
    contact = await db.execute(stmt)
    return contact.scalar_one_or_none()

