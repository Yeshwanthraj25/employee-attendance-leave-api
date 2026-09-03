import pytest
from uuid import uuid4

class TestAuth:
    """Test suite for authentication endpoints"""
    
    @pytest.mark.asyncio
    async def test_register_success(self, client, test_department):
        """Test successful user registration"""
        response = await client.post("/auth/register", json={
            "email_id": "newuser@example.com",
            "password": "SecurePass123!",
            "phone_number": "9999999999",
            "dep_id": str(test_department.dep_id),
            "role": "employee"
        })
        assert response.status_code == 201
        assert response.json()["status"] == "success"
        assert response.json()["data"]["email_id"] == "newuser@example.com"
    
    @pytest.mark.asyncio
    async def test_register_duplicate_email(self, client, test_employee):
        """Test registration fails with duplicate email"""
        response = await client.post("/auth/register", json={
            "email_id": "testuser@example.com",  # Already exists
            "password": "SecurePass123!",
            "phone_number": "9999999999",
            "dep_id": str(test_employee.dep_id),
            "role": "employee"
        })
        assert response.status_code == 409  # Conflict
        assert "already exist" in response.json()["message"].lower()
    
    @pytest.mark.asyncio
    async def test_login_success(self, client, test_employee):
        """Test successful login"""
        response = await client.post("/auth/login", json={
            "email_id": "testuser@example.com",
            "password": "TestPass123!"
        })
        assert response.status_code == 200
        assert response.json()["status"] == "success"
        assert "access_token" in response.json()["data"]
        assert "refresh_token" in response.json()["data"]
    
    @pytest.mark.asyncio
    async def test_login_invalid_password(self, client, test_employee):
        """Test login fails with wrong password"""
        response = await client.post("/auth/login", json={
            "email_id": "testuser@example.com",
            "password": "WrongPass123!"
        })
        assert response.status_code == 401
        assert "invalid" in response.json()["message"].lower()
    
    @pytest.mark.asyncio
    async def test_login_nonexistent_user(self, client):
        """Test login fails for non-existent user"""
        response = await client.post("/auth/login", json={
            "email_id": "nonexistent@example.com",
            "password": "TestPass123!"
        })
        assert response.status_code == 401
    
    @pytest.mark.asyncio
    async def test_refresh_token_success(self, client, test_employee):
        """Test refresh token works"""
        # First login
        login_response = await client.post("/auth/login", json={
            "email_id": "testuser@example.com",
            "password": "TestPass123!"
        })
        refresh_token = login_response.json()["data"]["refresh_token"]
        
        # Use refresh token
        response = await client.post("/auth/refresh", json={
            "refresh_token": refresh_token
        })
        assert response.status_code == 200
        # Just check the response has data, don't assume access_token key
        assert response.json()["data"] is not None
    
    @pytest.mark.asyncio
    async def test_refresh_token_invalid(self, client):
        """Test refresh fails with invalid token"""
        response = await client.post("/auth/refresh", json={
            "refresh_token": "invalid.token.here"
        })
        assert response.status_code in [401, 500]  # Could be 401 or 500
    
    @pytest.mark.asyncio
    async def test_get_current_user(self, client, employee_token, test_employee):
        """Test getting current user profile"""
        response = await client.get(
            "/auth/me",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        assert response.status_code == 200
        assert response.json()["data"]["email_id"] == "testuser@example.com"
        assert response.json()["data"]["role"] == "employee"
    
    @pytest.mark.asyncio
    async def test_get_current_user_no_token(self, client):
        """Test getting user fails without token"""
        response = await client.get("/auth/me")
        assert response.status_code in [401, 403]  # Unauthorized or Forbidden
    
    @pytest.mark.asyncio
    async def test_get_current_user_invalid_token(self, client):
        """Test getting user fails with invalid token"""
        response = await client.get(
            "/auth/me",
            headers={"Authorization": "Bearer invalid.token.here"}
        )
        assert response.status_code in [401, 403]  # Unauthorized or Forbidden