from utils.decorators import login_required, admin_required
from models.user import User


class DummyApp:
    def __init__(self, user=None):
        self.current_user = user

    @login_required
    def protected_action(self):
        return "Access granted"

    @admin_required
    def admin_action(self):
        return "Admin access granted"


def test_login_required_allows_logged_in_user():
    user = User("alice", "password", "User")
    app = DummyApp(user)

    assert app.protected_action() == "Access granted"


def test_login_required_blocks_logged_out_user(capsys):
    app = DummyApp()

    result = app.protected_action()

    captured = capsys.readouterr()

    assert result is None
    assert "Please login first." in captured.out


def test_admin_required_allows_admin():
    admin = User("admin", "password", "Admin")
    app = DummyApp(admin)

    assert app.admin_action() == "Admin access granted"


def test_admin_required_blocks_normal_user(capsys):
    user = User("alice", "password", "User")
    app = DummyApp(user)

    result = app.admin_action()

    captured = capsys.readouterr()

    assert result is None
    assert "Admin access required." in captured.out


def test_admin_required_blocks_logged_out_user(capsys):
    app = DummyApp()

    result = app.admin_action()

    captured = capsys.readouterr()

    assert result is None
    assert "Please login first." in captured.out