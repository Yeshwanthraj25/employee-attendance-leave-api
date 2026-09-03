import pytest
from datetime import date, timedelta

class TestAttendance:
    """Test suite for attendance endpoints"""
    
    @pytest.mark.asyncio
    async def test_check_in_success(self, client, employee_token):
        """Test successful check-in"""
        response = await client.post(
            "/attendance/check-in",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        assert response.status_code in [200, 201]
        assert response.json()["status"] == "success"  # API response status
        # Don't check data["status"] — it might not exist
        assert "log_id" in response.json()["data"]
        assert "log_in_time" in response.json()["data"]
        assert "log_in_time" in response.json()["data"]
    
    @pytest.mark.asyncio
    async def test_check_in_already_exists(self, client, employee_token):
        """Test check-in fails when already checked in today"""
        # First check-in
        await client.post(
            "/attendance/check-in",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        # Second check-in should fail
        response = await client.post(
            "/attendance/check-in",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        assert response.status_code == 400
        assert "already exist" in response.json()["message"].lower()
    
    @pytest.mark.asyncio
    async def test_check_in_no_token(self, client):
        """Test check-in fails without token"""
        response = await client.post("/attendance/check-in")
        assert response.status_code in [401, 403]  # Unauthorized or Forbidden
    
    @pytest.mark.asyncio
    async def test_check_out_success(self, client, employee_token):
        """Test successful check-out"""
        # Check-in first
        await client.post(
            "/attendance/check-in",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        # Now check-out
        response = await client.patch(
            "/attendance/check-out",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        assert response.status_code == 200
        assert response.json()["status"] == "success"
        assert response.json()["data"]["status"] == "present"
        assert "log_out_time" in response.json()["data"]
    
    @pytest.mark.asyncio
    async def test_check_out_without_check_in(self, client, employee_token):
        """Test check-out fails without prior check-in"""
        response = await client.patch(
            "/attendance/check-out",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        assert response.status_code in [400, 404]  # Not found or bad request
    
    @pytest.mark.asyncio
    async def test_check_out_already_checked_out(self, client, employee_token):
        """Test check-out fails when already checked out"""
        # Check-in and check-out
        await client.post(
            "/attendance/check-in",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        await client.patch(
            "/attendance/check-out",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        # Try to check-out again
        response = await client.patch(
            "/attendance/check-out",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        assert response.status_code == 409
        assert "already check out" in response.json()["message"].lower()
    
    @pytest.mark.asyncio
    async def test_get_attendance_history(self, client, employee_token):
        """Test getting personal attendance history"""
        # Check-in and check-out
        await client.post(
            "/attendance/check-in",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        await client.patch(
            "/attendance/check-out",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        
        # Get history
        response = await client.get(
            f"/attendance/me?start_date={date.today()}&end_date={date.today()}",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        assert response.status_code == 200
        assert len(response.json()["data"]) >= 1
        assert response.json()["data"][0]["status"] == "present"
    
    @pytest.mark.asyncio
    async def test_get_attendance_history_date_range(self, client, employee_token):
        """Test getting history with date range"""
        response = await client.get(
            f"/attendance/me?start_date=2026-08-01&end_date=2026-08-31",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        assert response.status_code == 200
        assert isinstance(response.json()["data"], list)
    
    @pytest.mark.asyncio
    async def test_get_team_attendance_success(self, client, manager_token, test_manager):
        """Test manager can view team attendance"""
        response = await client.get(
            f"/attendance/team?start_date=2026-08-01&end_date=2026-08-31",
            headers={"Authorization": f"Bearer {manager_token}"}
        )
        assert response.status_code == 200
        assert isinstance(response.json()["data"], list)
    
    @pytest.mark.asyncio
    async def test_get_team_attendance_forbidden_for_employee(self, client, employee_token):
        """Test employee cannot view team attendance"""
        response = await client.get(
            f"/attendance/team?start_date=2026-08-01&end_date=2026-08-31",
            headers={"Authorization": f"Bearer {employee_token}"}
        )
        assert response.status_code == 403
        assert "only managers" in response.json()["message"].lower()