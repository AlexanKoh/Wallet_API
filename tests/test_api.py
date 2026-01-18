import pytest
import uuid
from app import crud

@pytest.mark.asyncio
async def test_get_nonexistent_wallet(client):
    wallet_id = uuid.uuid4()
    response = await client.get(f"/api/v1/wallets/{wallet_id}")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_create_and_get_wallet(client, db_session):
    wallet = await crud.create_wallet(db_session)
    
    response = await client.get(f"/api/v1/wallets/{wallet.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(wallet.id)
    assert data["balance"] == "0.00"

@pytest.mark.asyncio
async def test_deposit(client, db_session):
    wallet = await crud.create_wallet(db_session)
    
    response = await client.post(
        f"/api/v1/wallets/{wallet.id}/operation",
        json={"operation_type": "DEPOSIT", "amount": "100.50"}
    )
    assert response.status_code == 200
    
    response = await client.get(f"/api/v1/wallets/{wallet.id}")
    assert response.json()["balance"] == "100.50"

@pytest.mark.asyncio
async def test_withdraw_insufficient_funds(client, db_session):
    wallet = await crud.create_wallet(db_session)
    
    response = await client.post(
        f"/api/v1/wallets/{wallet.id}/operation",
        json={"operation_type": "WITHDRAW", "amount": "50.00"}
    )
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_deposit_and_withdraw(client, db_session):
    wallet = await crud.create_wallet(db_session)

    await client.post(
        f"/api/v1/wallets/{wallet.id}/operation",
        json={"operation_type": "DEPOSIT", "amount": "200.00"}
    )

    response = await client.post(
        f"/api/v1/wallets/{wallet.id}/operation",
        json={"operation_type": "WITHDRAW", "amount": "150.00"}
    )
    assert response.status_code == 200
    
    response = await client.get(f"/api/v1/wallets/{wallet.id}")
    assert response.json()["balance"] == "50.00"
