from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app import models
import uuid
from decimal import Decimal

async def get_wallet(db: AsyncSession, wallet_id: uuid.UUID):
    result = await db.execute(
        select(models.Wallet).where(models.Wallet.id == wallet_id)
    )
    return result.scalar_one_or_none()

async def create_wallet(db: AsyncSession):
    wallet = models.Wallet()
    db.add(wallet)
    await db.commit()
    await db.refresh(wallet)
    return wallet

async def update_wallet_balance(db: AsyncSession, wallet_id: uuid.UUID, amount: Decimal, operation_type: str):
    stmt = (
        select(models.Wallet)
        .where(models.Wallet.id == wallet_id)
        .with_for_update()
    )
    result = await db.execute(stmt)
    wallet = result.scalar_one_or_none()
    
    if not wallet:
        return None
    
    if operation_type == "DEPOSIT":
        new_balance = wallet.balance + amount
    else:
        if wallet.balance < amount:
            return None
        new_balance = wallet.balance - amount

    wallet.balance = new_balance
    await db.commit()
    await db.refresh(wallet)

    operation = models.Operation(
        wallet_id=wallet_id,
        operation_type=operation_type,
        amount=amount
    )
    db.add(operation)
    await db.commit()
    
    return wallet
