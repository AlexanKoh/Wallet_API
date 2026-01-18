from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, schemas
from app.database import get_db
from app.dependencies import get_wallet_or_404
from app.utils import validate_amount
import uuid
from decimal import Decimal

router = APIRouter()

@router.get("/wallets/{wallet_id}", response_model=schemas.WalletResponse)
async def get_wallet_balance(
    wallet = Depends(get_wallet_or_404)
):
    return wallet

@router.post("/wallets/{wallet_id}/operation")
async def wallet_operation(
    wallet_id: uuid.UUID,
    operation: schemas.OperationCreate,
    db: AsyncSession = Depends(get_db)
):
    validate_amount(operation.amount)
    
    if operation.operation_type == "WITHDRAW":
        wallet = await crud.get_wallet(db, wallet_id)
        if not wallet:
            raise HTTPException(status_code=404, detail="Wallet not found")
    
    updated_wallet = await crud.update_wallet_balance(
        db, wallet_id, operation.amount, operation.operation_type
    )
    
    if not updated_wallet:
        if operation.operation_type == "WITHDRAW":
            raise HTTPException(status_code=400, detail="Insufficient funds")
        raise HTTPException(status_code=404, detail="Wallet not found")
    
    return {"message": "Operation successful", "balance": updated_wallet.balance}
    
@router.post("/wallets", response_model=schemas.WalletResponse, status_code=201)
async def create_wallet(db: AsyncSession = Depends(get_db)):
    """Создание нового кошелька"""
    wallet = await crud.create_wallet(db)
    return wallet
