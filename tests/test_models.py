import pytest
from app.models import Wallet, Operation
import uuid

def test_wallet_creation():
    wallet = Wallet()
    assert wallet.id is not None
    assert wallet.balance == 0

def test_operation_creation():
    operation = Operation(
        wallet_id=uuid.uuid4(),
        operation_type="DEPOSIT",
        amount=100.50
    )
    assert operation.id is not None
    assert operation.operation_type == "DEPOSIT"
    assert operation.amount == 100.50
