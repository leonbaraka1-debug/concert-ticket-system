import pytest
import os
from models.user import User, register_user, login_user, load_users, save_users, USERS_FILE

# Test fixture that ensures a pristine test environment by clearing the JSON file before and after each test
@pytest.fixture(autouse=True)
def clean_users_file():
    if os.path.exists(USERS_FILE):
        os.remove(USERS_FILE)
    yield
    if os.path.exists(USERS_FILE):
        os.remove(USERS_FILE)

# Validates that a User instance initializes attributes properly and securely hashes passwords
def test_user_creation():
    user = User("alice", "password123", "Admin")
    assert user.username == "alice"
    assert user.role == "Admin"
    assert user.check_password("password123")
    assert not user.check_password("wrongpassword")

# Tests object serialization to dictionary and deserialization back into a User instance
def test_user_to_from_dict():
    user = User("bob", "secret", "User")
    data = user.to_dict()
    new_user = User.from_dict(data)
    assert new_user.username == "bob"
    assert new_user.role == "User"
    assert new_user.password_hash == user.password_hash

# Tests successful user registration and checks that duplicate usernames are rejected
def test_register_user():
    success, msg = register_user("charlie", "mypass123", "User")
    assert success
    
    users = load_users()
    assert "charlie" in users
    
    # Try duplicate registration
    success2, msg2 = register_user("charlie", "mypass123", "User")
    assert not success2

# Tests authentication flows for valid credentials, wrong passwords, and nonexistent users
def test_login_user():
    register_user("dave", "securepass")
    
    success, user = login_user("dave", "securepass")
    assert success
    assert user.username == "dave"
    
    success_fail, _ = login_user("dave", "wrongpass")
    assert not success_fail
    
    success_nf, _ = login_user("nonexistent", "securepass")
    assert not success_nf