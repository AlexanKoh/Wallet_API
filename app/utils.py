from fastapi import HTTPException
from decimal import Decimal

def validate_amount(amount: Decimal):
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    if amount.as_tuple().exponent < -2:
        raise HTTPException(status_code=400, detail="Maximum 2 decimal places allowed")
