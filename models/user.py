import hashlib
import json
import os

class User:
    def __init__(self, username, password, role="User"):
        self.username = username
        self.password_hash = self._hash_password(password)
        self.role = role  # "Admin" or "User"

    @staticmethod
    def _hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password):
        return self.password_hash == self._hash_password(password)

    def to_dict(self):
        return {
            "username": self.username,
            "password_hash": self.password_hash,
            "role": self.role
        }

    @classmethod
    def from_dict(cls, data):
        user = cls(data["username"], "", data.get("role", "User"))
        user.password_hash = data["password_hash"]
        return user


USERS_FILE = os.path.join("data", "users.json")

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, "r") as f:
            data = json.load(f)
            return {username: User.from_dict(info) for username, info in data.items()}
    except json.JSONDecodeError:
        return {}

def save_users(users_dict):
    os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
    with open(USERS_FILE, "w") as f:
        data = {username: user.to_dict() for username, user in users_dict.items()}
        json.dump(data, f, indent=4)

def register_user(username, password, role="User"):
    users = load_users()
    if not username or not password:
        return False, "Username and password cannot be empty."
    if username in users:
        return False, "Username already exists."
    
    users[username] = User(username, password, role)
    save_users(users)
    return True, "Registration successful!"

def login_user(username, password):
    users = load_users()
    if username not in users:
        return False, "User not found."
    
    user = users[username]
    if user.check_password(password):
        return True, user
    return False, "Incorrect password."