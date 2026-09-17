import pytest

from models.user import (User, register_user, login_user, load_users, save_users)

@pytest.fixture
def users_file(tmp_path):
    return str(tmp_path / "users.json")


def test_user_creation():
    user = User("alice", "password123", "Admin")

    assert user.username == "alice"
    assert user.role == "Admin"
    assert user.check_password("password123")
    assert not user.check_password("wrongpassword")


def test_user_to_from_dict():
    user = User("bob", "secret", "User")

    data = user.to_dict()
    new_user = User.from_dict(data)

    assert new_user.username == "bob"
    assert new_user.role == "User"
    assert new_user.password_hash == user.password_hash


def test_register_user(users_file):
    success, msg = register_user(
        "charlie",
        "mypass123",
        filepath=users_file
    )

    assert success

    users = load_users(users_file)

    assert "charlie" in users

    success2, msg2 = register_user(
        "charlie",
        "mypass123",
        filepath=users_file
    )

    assert not success2


def test_register_user_cannot_self_assign_admin(users_file):
    """
    Regression test for bug 6: register_user() must not accept a role
    argument at all, so there is no way for a new signup to become Admin.
    """
    register_user("eve", "evepass", filepath=users_file)

    users = load_users(users_file)
    assert users["eve"].role == "User"

    # confirm the function signature itself has no room for a role —
    # calling it with a role positionally/by keyword should fail outright
    with pytest.raises(TypeError):
        register_user("mallory", "mallorypass", "Admin", filepath=users_file)

    with pytest.raises(TypeError):
        register_user("mallory2", "mallorypass", role="Admin", filepath=users_file)


def test_login_user(users_file):
    register_user(
        "dave",
        "securepass",
        filepath=users_file
    )

    success, user = login_user(
        "dave",
        "securepass",
        filepath=users_file
    )

    assert success
    assert user.username == "dave"

    success_fail, _ = login_user(
        "dave",
        "wrongpass",
        filepath=users_file
    )

    assert not success_fail

    success_nf, _ = login_user(
        "nonexistent",
        "securepass",
        filepath=users_file
    )

    assert not success_nf


def test_save_users(users_file):
    user = User("alice", "password123", "Admin")

    users = {
        "alice": user
    }

    save_users(users, users_file)

    loaded_users = load_users(users_file)

    assert "alice" in loaded_users
    assert loaded_users["alice"].role == "Admin"
    assert loaded_users["alice"].check_password("password123")