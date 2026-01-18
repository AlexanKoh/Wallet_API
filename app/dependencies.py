from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app import crud
import uuid
from fastapi import HTTPException

async def get_wallet_or_404(
    wallet_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    wallet = await crud.get_wallet(db, wallet_id)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return wallet
