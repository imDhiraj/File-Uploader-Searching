# tests/test_auth.py
#it only run when it testin start in the name 
#tracseback give the why the error occured
import pytest

@pytest.mark.asyncio
async def test_user_registration_duplicate(async_client):
    # First registration
    await async_client.post("/api/v1/auth/signup", json={
        "username": "testuser7",
        "email": "testuser7@example.com",
        "password": "strongpassword"
    })

    # Attempt to register same user again
    response = await async_client.post("/api/v1/auth/signup", json={
        "username": "testuser7",
        "email": "testuser7@example.com",
        "password": "strongpassword"
    })

    assert response.status_code == 400
    assert "already exists" in response.text.lower()

@pytest.mark.asyncio
async def test_user_login_success(async_client):
    response = await async_client.post(
        "/api/v1/auth/login",
        data={
            "username": "testuser7",
            "password": "strongpassword"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    print("Status code:", response.status_code)
    print("Response:", response.text)

    assert response.status_code == 200
    assert "access_token" in response.text.lower()
