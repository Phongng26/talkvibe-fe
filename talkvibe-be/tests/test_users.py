"""
Tests for user-related functionality.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool
import asyncio
from typing import AsyncGenerator

from app.main import app
from app.core.database import get_db, Base
from app.models.user import User, EnglishLevel
from app.utils.auth import get_password_hash

# Test database URL (in-memory SQLite)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Create test engine
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestSessionLocal = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    """Override database dependency for testing."""
    async with TestSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# Override the dependency
app.dependency_overrides[get_db] = override_get_db

# Test client
client = TestClient(app)


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def setup_test_db():
    """Set up test database."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def test_user():
    """Create a test user."""
    async with TestSessionLocal() as session:
        user = User(
            name="Test User",
            email="test@example.com",
            hashed_password=get_password_hash("testpassword123"),
            english_level=EnglishLevel.INTERMEDIATE,
            bio="Test user bio",
            goals="Learn English"
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user


class TestUserRegistration:
    """Test user registration functionality."""
    
    def test_register_user_success(self):
        """Test successful user registration."""
        user_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "password": "SecurePass123!",
            "english_level": "beginner",
            "bio": "Learning English",
            "goals": "Improve speaking skills"
        }
        
        response = client.post("/api/users/register", json=user_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == user_data["email"]
        assert data["name"] == user_data["name"]
        assert data["english_level"] == user_data["english_level"]
        assert "id" in data
        assert "created_at" in data
    
    def test_register_user_duplicate_email(self):
        """Test registration with duplicate email."""
        user_data = {
            "name": "Jane Doe",
            "email": "john@example.com",  # Same email as previous test
            "password": "SecurePass123!",
            "english_level": "intermediate"
        }
        
        response = client.post("/api/users/register", json=user_data)
        
        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]
    
    def test_register_user_invalid_password(self):
        """Test registration with invalid password."""
        user_data = {
            "name": "Bob Smith",
            "email": "bob@example.com",
            "password": "weak",  # Too short
            "english_level": "beginner"
        }
        
        response = client.post("/api/users/register", json=user_data)
        
        assert response.status_code == 422  # Validation error


class TestUserLogin:
    """Test user login functionality."""
    
    def test_login_success(self):
        """Test successful login."""
        # First register a user
        user_data = {
            "name": "Login Test",
            "email": "login@example.com",
            "password": "LoginPass123!",
            "english_level": "advanced"
        }
        client.post("/api/users/register", json=user_data)
        
        # Then login
        login_data = {
            "username": "login@example.com",
            "password": "LoginPass123!"
        }
        
        response = client.post("/api/users/login", data=login_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "user" in data
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials."""
        login_data = {
            "username": "nonexistent@example.com",
            "password": "wrongpassword"
        }
        
        response = client.post("/api/users/login", data=login_data)
        
        assert response.status_code == 401
        assert "Incorrect email or password" in response.json()["detail"]


class TestUserProfile:
    """Test user profile functionality."""
    
    def test_get_profile_unauthorized(self):
        """Test getting profile without authentication."""
        response = client.get("/api/users/profile")
        
        assert response.status_code == 401
    
    def test_get_profile_success(self):
        """Test getting profile with valid token."""
        # Register and login
        user_data = {
            "name": "Profile Test",
            "email": "profile@example.com",
            "password": "ProfilePass123!",
            "english_level": "intermediate"
        }
        client.post("/api/users/register", json=user_data)
        
        login_response = client.post("/api/users/login", data={
            "username": "profile@example.com",
            "password": "ProfilePass123!"
        })
        token = login_response.json()["access_token"]
        
        # Get profile
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/api/users/profile", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == user_data["email"]
        assert data["name"] == user_data["name"]


if __name__ == "__main__":
    pytest.main([__file__])
