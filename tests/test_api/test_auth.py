from fastapi.testclient import TestClient

def test_register_user(client: TestClient):
    """
    Test user registration endpoint.
    """
    email = "test@example.com"
    password = "secretpassword"
    
    response = client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": password, "is_active": True},
    )
    
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["email"] == email
    # Check that ID exists and it's an integer
    assert "id" in data
    # Password should never be returned!
    assert "hashed_password" not in data
    assert "password" not in data

def test_login_access_token(client: TestClient):
    """
    Test user login and token generation.
    """
    # 1. Register a user first (we can use the API itself or the DB fixture directly,
    # but using the API is simpler for this integration test)
    email = "login@example.com"
    password = "secretpassword"
    client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": password, "is_active": True},
    )
    
    # 2. Attempt to login
    login_data = {"email": email, "password": password}
    response = client.post("/api/v1/auth/login", json=login_data)
    
    assert response.status_code == 200, response.text
    tokens = response.json()
    assert "access_token" in tokens
    assert tokens["access_token"]
    assert tokens["token_type"] == "bearer"

def test_test_token(client: TestClient):
    """
    Test the endpoint that requires an authenticated user.
    """
    # 1. Register and Login to get a token
    email = "testtoken@example.com"
    password = "secretpassword"
    client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": password, "is_active": True},
    )
    login_response = client.post(
        "/api/v1/auth/login", json={"email": email, "password": password}
    )
    token = login_response.json()["access_token"]
    
    # 2. Access the protected endpoint by adding the token to the header
    response = client.post(
        "/api/v1/auth/test-token",
        headers={"Authorization": f"Bearer {token}"},
    )
    
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == email
    
def test_test_token_fails_without_auth(client: TestClient):
    """
    Verifies that accessing a protected route without a token fails with a 403.
    """
    response = client.post("/api/v1/auth/test-token")
    assert response.status_code == 403
