import pytest
from fastapi.testclient import TestClient

@pytest.fixture
def user_token_headers(client: TestClient) -> dict:
    """
    A helper fixture to register a user, log them in, and return
    the authorization headers. This makes writing other tests much easier!
    """
    email = "todo_tester@example.com"
    password = "secretpassword"
    
    client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": password, "is_active": True},
    )
    
    login_response = client.post(
        "/api/v1/auth/access-token", data={"username": email, "password": password}
    )
    token = login_response.json()["access_token"]
    
    return {"Authorization": f"Bearer {token}"}

def test_create_todo(client: TestClient, user_token_headers: dict):
    """
    Test creating a new todo item.
    """
    data = {"title": "Buy Milk", "description": "2% fat", "is_completed": False}
    response = client.post(
        "/api/v1/todos/", headers=user_token_headers, json=data
    )
    
    assert response.status_code == 201, response.text
    content = response.json()
    assert content["title"] == data["title"]
    assert content["description"] == data["description"]
    assert "id" in content
    assert "owner_id" in content

def test_read_todos(client: TestClient, user_token_headers: dict):
    """
    Test retrieving a list of todos.
    """
    # Create two todos
    client.post(
        "/api/v1/todos/", headers=user_token_headers, json={"title": "Task 1"}
    )
    client.post(
        "/api/v1/todos/", headers=user_token_headers, json={"title": "Task 2"}
    )
    
    response = client.get("/api/v1/todos/", headers=user_token_headers)
    
    assert response.status_code == 200, response.text
    content = response.json()
    assert isinstance(content, list)
    assert len(content) >= 2 # Might be more if previous tests polluted, but we use transactions

def test_update_todo(client: TestClient, user_token_headers: dict):
    """
    Test updating an existing todo item.
    """
    # 1. Create it
    create_resp = client.post(
        "/api/v1/todos/", headers=user_token_headers, json={"title": "Old Title"}
    )
    todo_id = create_resp.json()["id"]
    
    # 2. Update it
    update_data = {"title": "New Title", "is_completed": True}
    response = client.put(
        f"/api/v1/todos/{todo_id}", headers=user_token_headers, json=update_data
    )
    
    assert response.status_code == 200, response.text
    content = response.json()
    assert content["title"] == "New Title"
    assert content["is_completed"] is True
    # Verify description remained untouched (default None)
    assert content["description"] is None

def test_delete_todo(client: TestClient, user_token_headers: dict):
    """
    Test deleting an existing todo item.
    """
    # 1. Create it
    create_resp = client.post(
        "/api/v1/todos/", headers=user_token_headers, json={"title": "To Delete"}
    )
    todo_id = create_resp.json()["id"]
    
    # 2. Delete it
    delete_response = client.delete(
        f"/api/v1/todos/{todo_id}", headers=user_token_headers
    )
    assert delete_response.status_code == 200, delete_response.text
    
    # 3. Verify it's gone by trying to update it (which should return 404)
    verify_response = client.put(
        f"/api/v1/todos/{todo_id}", headers=user_token_headers, json={"title": "Deleted"}
    )
    assert verify_response.status_code == 404
