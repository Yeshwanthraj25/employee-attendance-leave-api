import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from src.main import app
from src.repository.Database import get_db
from src.repository.schema.schema import Base, Employee, LeaveQuote, Department
from src.core.security import hash_password
from uuid import uuid4
from datetime import datetime, date
from unittest.mock import AsyncMock, patch



from unittest.mock import AsyncMock, patch

@pytest.fixture(autouse=True)
async def mock_error_logging():
    """Mock error_insert to prevent database errors during tests"""
    with patch('src.repository.error_repo.error_insert', new_callable=AsyncMock) as mock_insert:
        mock_insert.return_value = None
        yield mock_insert

# Test database URL — UPDATE WITH YOUR CREDENTIALS
TEST_DB_URL = "postgresql+asyncpg://postgres:admin%40123@localhost:5432/attendance_db_test"

@pytest.fixture(autouse=True)
async def mock_error_logging():
    """Mock error logging to avoid database issues in tests"""
    with patch('src.repository.error_repo.error_insert', new_callable=AsyncMock):
        yield

@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()

@pytest.fixture
async def test_db(event_loop):
    """Create test database and tables"""
    engine = create_async_engine(TEST_DB_URL, echo=False)
    
    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Create session factory
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    # Create session
    async with async_session() as session:
        yield session
    
    # Drop all tables after test
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()

@pytest.fixture
async def client(test_db):
    """Async HTTP client for testing"""
    async def override_get_db():
        yield test_db
    
    app.dependency_overrides[get_db] = override_get_db
    
    # Use ASGITransport for newer httpx versions
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()

@pytest.fixture
async def test_department(test_db):
    """Create a test department"""
    dept = Department(
        dep_id=uuid4(),
        dep_name="Engineering",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    test_db.add(dept)
    await test_db.flush()
    await test_db.commit()
    return dept

@pytest.fixture
async def test_employee(test_db, test_department):
    """Create a test employee"""
    emp = Employee(
        emp_id=uuid4(),
        email_id="testuser@example.com",
        password=hash_password("TestPass123!"),
        phone_number="9876543210",
        role="employee",
        dep_id=test_department.dep_id,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    test_db.add(emp)
    await test_db.flush()
    await test_db.commit()
    return emp

@pytest.fixture
async def test_manager(test_db, test_department):
    """Create a test manager user"""
    manager = Employee(
        emp_id=uuid4(),
        email_id="manager@example.com",
        password=hash_password("ManagerPass123!"),
        phone_number="9876543211",
        role="manager",
        dep_id=test_department.dep_id,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    test_db.add(manager)
    await test_db.flush()
    await test_db.commit()
    return manager

@pytest.fixture
async def employee_token(client, test_employee):
    """Get JWT token for test employee"""
    response = await client.post("/auth/login", json={
        "email_id": "testuser@example.com",
        "password": "TestPass123!"
    })
    return response.json()["data"]["access_token"]

@pytest.fixture
async def manager_token(client, test_manager):
    """Get JWT token for test manager"""
    response = await client.post("/auth/login", json={
        "email_id": "manager@example.com",
        "password": "ManagerPass123!"
    })
    return response.json()["data"]["access_token"]

@pytest.fixture
async def test_leave_quota(test_db, test_employee):
    """Create a leave quota for the test employee"""
    quota = LeaveQuote(
        quote_id=uuid4(),
        emp_id=test_employee.emp_id,
        year=2026,
        sick_leave_allotted=12,
        sick_leave_remaining=12,
        casual_leave_allotted=10,
        casual_leave_remaining=10,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    test_db.add(quota)
    await test_db.flush()
    await test_db.commit()
    return quota