from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
import uuid
from decimal import Decimal
from datetime import datetime

class OperationCreate(BaseModel):
    operation_type: str = Field(..., pattern="^(DEPOSIT|WITHDRAW)$")
    amount: Decimal = Field(..., gt=0)

class WalletResponse(BaseModel):
    id: uuid.UUID
    balance: Decimal
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)
